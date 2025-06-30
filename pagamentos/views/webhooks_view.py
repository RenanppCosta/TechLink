from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

from pagamentos.models import Pagamento

# VAI SER USADO QUANDO TIVERMOS O BANCO DE DADOS!!
# Arquivo: pagamentos/views.py

@csrf_exempt
def abacate_pay_webhook(request):
    """
    Recebe a notificação de pagamento do Abacate Pay e atualiza o status no nosso sistema.
    """
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)

    try:
        data = json.loads(request.body)
        event_type = data.get('event')

        # Verifique na documentação do Abacate Pay o nome exato do evento de pagamento confirmado
        if event_type == 'pix_qrcode_paid': 
            charge_data = data.get('data', {})
            
            # Usamos o ID que passamos ao criar a cobrança para encontrar nosso registro de pagamento
            pagamento_id_interno = charge_data.get('external_id')
            
            if not pagamento_id_interno:
                return JsonResponse({'status': 'error', 'message': 'ID externo não encontrado no webhook'}, status=400)

            try:
                # Encontra o pagamento que estava pendente
                pagamento = Pagamento.objects.get(id=pagamento_id_interno, status='pendente')
                
                # ATUALIZA O STATUS PARA PAGO!
                pagamento.status = 'pago'
                pagamento.save()
                
                # Neste ponto, você poderia enviar um e-mail de confirmação para o aluno, etc.
                
                return JsonResponse({'status': 'success'})

            except Pagamento.DoesNotExist:
                # O pagamento não foi encontrado ou já foi processado.
                return JsonResponse({'status': 'error', 'message': 'Pagamento não encontrado ou já processado'}, status=404)
                
    except json.JSONDecodeError:
        return JsonResponse({'status': 'error', 'message': 'JSON inválido'}, status=400)
    except Exception as e:
        # Em produção, logue este erro
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)

    return JsonResponse({'status': 'ok', 'message': 'Evento não processado'})
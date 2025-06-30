# ... todos os seus imports ...
import traceback
import requests
import stripe
import json
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from agendamentos.models import Aula, Horario
from pagamentos.models import Pagamento 

@csrf_exempt
def create_payment(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)

    try:
        data = json.loads(request.body)
        payment_method = data.get('payment_method')
        amount_in_cents = data.get('amount')
        horario_ids = data.get('horario_ids')
        aluno_perfil = request.user.aluno_profile

        if not all([payment_method, amount_in_cents, horario_ids, aluno_perfil]):
            return JsonResponse({'error': 'Dados insuficientes na requisição'}, status=400)

        # --- FLUXO DO CARTÃO (JÁ ESTÁ FUNCIONANDO) ---
        if payment_method == 'card':
            stripe.api_key = settings.STRIPE_API_KEY
            intent = stripe.PaymentIntent.create(
                amount=amount_in_cents,
                currency="brl",
                metadata={"horario_ids": json.dumps(horario_ids)}
            )
            return JsonResponse({"clientSecret": intent.client_secret})

        # --- FLUXO DO PIX (AGORA CORRIGIDO E INTEGRADO) ---
        elif payment_method == 'pix':
            # 1. Cria um registro de pagamento interno com status 'pendente'
            # Isso é crucial para que o webhook saiba qual agendamento confirmar depois
            pagamento_pendente = Pagamento.objects.create(
                aluno=aluno_perfil,
                valor=amount_in_cents / 100.0,
                status='pendente',
                metodo_pagamento='pix'
            )
            
            # Linka as aulas a este pagamento pendente
            horarios = Horario.objects.filter(id__in=horario_ids)
            for horario in horarios:
                 Aula.objects.create(
                    horario=horario,
                    aluno=aluno_perfil,
                    professor=horario.professor,
                    pagamento=pagamento_pendente
                )
                 # Marca o horário como indisponível para evitar que outra pessoa agende
                 horario.disponivel = False
                 horario.save()


            # 2. Chama a API do Abacate Pay para gerar o QR Code
            pix_creation_url = "https://api.abacatepay.com/v1/pixQrCode/create"
            payload = {
                # O Abacate Pay espera o valor em centavos
                "amount": amount_in_cents,
                # Passamos nosso ID de pagamento para o Abacate Pay nos retornar no webhook
                "external_id": str(pagamento_pendente.id)
            }
            headers = {
                "Authorization": f"Bearer {settings.ABACATE_PAY_API_KEY}",
                "Content-Type": "application/json"
            }

            response = requests.post(pix_creation_url, json=payload, headers=headers)
            response_data = response.json()
            
            if response.status_code >= 400:
                # Se falhar, reverte a criação do pagamento e aulas
                pagamento_pendente.delete() 
                return JsonResponse({'error': response_data}, status=400)

            # 3. Atualiza nosso pagamento com o ID da transação do Abacate Pay
            data_object = response_data.get('data', {})
            charge_id = data_object.get("id")
            if charge_id:
                pagamento_pendente.id_transacao_provedor = charge_id
                pagamento_pendente.save()

            # 4. Retorna os dados do QR Code para o frontend
            pix_data = {
                "qr_code_image": data_object.get("brCodeBase64"),
                "qr_code_text": data_object.get("brCode"),
            }
            
            if not pix_data["qr_code_image"] or not pix_data["qr_code_text"]:
                return JsonResponse({'error': 'A resposta da API do Pix não continha os dados do QR Code.'}, status=500)
            
            print("\n\n--- DADOS PARA TESTAR NO ABACATE PAY ---")
            print(f"🔑 Bearer Token (Sua API Key): {settings.ABACATE_PAY_API_KEY}")
            print(f"🧾 ID do QRcode Pix (charge_id): {charge_id}")
            
            return JsonResponse(pix_data)

        else:
            return JsonResponse({'error': 'Método de pagamento inválido'}, status=400)

    except Exception as e:
        # A lógica de depuração que tínhamos
        print("----------- ERRO NA CRIAÇÃO DO PAGAMENTO -----------")
        print(f"O erro foi: {e}")
        print(traceback.format_exc())
        print("--------------------------------------------------")
        return JsonResponse({'error': str(e)}, status=500)


def payment_success_view(request):
    """Confirma o pagamento, cria o objeto Pagamento e as Aulas vinculadas."""
    payment_intent_id = request.GET.get('payment_intent')
    if not payment_intent_id:
        return redirect('techlink:home') # Altere para sua URL de início

    try:
        if Pagamento.objects.filter(id_transacao_provedor=payment_intent_id).exists():
            return render(request, 'pagamentos/payment_success.html')

        stripe.api_key = settings.STRIPE_API_KEY
        intent = stripe.PaymentIntent.retrieve(payment_intent_id)

        if intent.status == 'succeeded':
            novo_pagamento = Pagamento.objects.create(
                aluno=request.user.aluno_profile,
                valor=intent.amount / 100.0,
                status='pago',
                id_transacao_provedor=payment_intent_id,
                metodo_pagamento=intent.payment_method_types[0]
            )

            metadata = intent.metadata
            horario_ids = json.loads(metadata.get('horario_ids', '[]'))
            horarios = Horario.objects.filter(id__in=horario_ids, disponivel=True)

            for horario in horarios:
                Aula.objects.create(
                    horario=horario,
                    aluno=request.user.aluno_profile,
                    professor=horario.professor,
                    pagamento=novo_pagamento # Vincula a aula ao pagamento
                )
                horario.disponivel = False
                horario.save()
            
            if 'checkout_context' in request.session:
                del request.session['checkout_context']

            return render(request, 'pagamentos/payment_success.html')
        else:
            return redirect('techlink:home') # Ou para uma página de falha

    
    except Exception as e:
        # ---- ADIÇÃO PARA DEPURAÇÃO ----
        print("----------- ERRO NA VIEW DE SUCESSO -----------")
        print(f"O erro foi: {e}")
        print(traceback.format_exc()) # Imprime o traceback completo
        print("---------------------------------------------")
        # ----------------------------------
        return redirect('techlink:home') # A view continua redirecionando para a home
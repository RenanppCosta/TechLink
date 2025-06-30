from django.views import View
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import PerfilProfessor, PerfilAluno
from .models import Horario, Aula


class CriarAgendamentoView(LoginRequiredMixin, View):
    def post(self, request, professor_id):
        professor = get_object_or_404(PerfilProfessor, id=professor_id)
        horarios_selecionados_str = request.POST.get("horarios", "")
        
        if not horarios_selecionados_str:
            return redirect('accounts:professor_detail', pk=professor.id)

        horarios_str_list = horarios_selecionados_str.split(",")
        horario_ids = []
        
        for horario_str in horarios_str_list:
            try:
                dia, hora = horario_str.rsplit("-", 1)
                data = dia_para_data(dia)
                horario_obj = Horario.objects.get(professor=professor, data=data, hora=hora, disponivel=True)
                horario_ids.append(horario_obj.id)
            except Horario.DoesNotExist:
                continue

        if not horario_ids:
            return redirect('accounts:professor_detail', pk=professor.id)

        valor_total = len(horario_ids) * professor.valor_hora

        # A PARTE MAIS IMPORTANTE: SALVAR TUDO NA SESSÃO
        request.session['checkout_context'] = {
            'professor_id': professor.id,
            'horario_ids': horario_ids,
            'valor_total': float(valor_total),
            'valor_em_centavos': int(valor_total * 100)
        }

        return redirect('pagamentos:pagamentos')
    
class AulaConcluirView(LoginRequiredMixin, View):
    def post(self, request, aula_id):
        aula = get_object_or_404(Aula, id=aula_id)
        aula.status = 'realizada'
        aula.save()
        return redirect('accounts:self_user_profile')
    
class AulaCancelarView(LoginRequiredMixin, View):
    def post(self, request, aula_id):
        aula = get_object_or_404(Aula, id=aula_id)
        aula.status = 'cancelada'
        aula.save()
        aula.horario.disponivel = True
        aula.horario.save()
        return redirect('accounts:self_user_profile')

class AulaExcluirView(LoginRequiredMixin, View):
    def post(self, request, aula_id):
        aula = get_object_or_404(Aula, id=aula_id)
        aula.delete()
        return redirect('accounts:self_user_profile')

# Função utilitária (exemplo) para converter "Seg 24/06" em date:
from datetime import datetime
def dia_para_data(dia_str):
    # Exemplo: "Seg 24/06"
    return datetime.strptime(dia_str.split(" ")[1], "%d/%m").replace(year=datetime.today().year).date()
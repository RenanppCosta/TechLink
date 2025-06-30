from django.views import View
from django.shortcuts import redirect, get_object_or_404, render
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import PerfilProfessor, PerfilAluno
from .models import Horario, Aula


class CriarAgendamentoView(LoginRequiredMixin, View):
    def post(self, request, professor_id):
        professor = get_object_or_404(PerfilProfessor, id=professor_id)
        try:
            aluno = request.user.aluno_profile  # <-- use o related_name correto
        except PerfilAluno.DoesNotExist:
            return render(request, 'profiles/professor_detail.html', {
                'perfil_professor': professor,
                'erro_permissao': True,
                # Adicione outros contextos necessários para renderizar a agenda corretamente
            })

        horarios_str = request.POST.get("horarios", "")
        horarios_list = horarios_str.split(",")
        for horario_str in horarios_list:
            dia, hora = horario_str.rsplit("-", 1)
            data = dia_para_data(dia)
            try:
                horario = Horario.objects.get(
                    professor=professor,
                    data=data,
                    hora=hora,
                    disponivel=True  # só permite se estiver disponível!
                )
            except Horario.DoesNotExist:
                continue  # ou retorne erro para o usuário
            horario.disponivel = False
            horario.save()
            Aula.objects.create(
                horario=horario,
                aluno=aluno,
                professor=professor,
                pago=False
            )
        return redirect('accounts:professor_detail', pk=professor.id)
    
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
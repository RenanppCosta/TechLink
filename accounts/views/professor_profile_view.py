from django.views.generic.detail import DetailView
from accounts.models import PerfilProfessor
from agendamentos.models import Horario
from datetime import datetime, timedelta, time

class ProfessorDetailView(DetailView):
    model = PerfilProfessor
    template_name = 'profiles/professor_detail.html'
    context_object_name = 'perfil_professor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        hoje = datetime.today().date()
        dias = []
        dias_labels = []
        for i in range(7):
            data = hoje + timedelta(days=i)
            nome_dia_pt = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom'][data.weekday()]
            dias.append(data)
            dias_labels.append(f"{nome_dia_pt} {data.day:02d}/{data.month:02d}")

        horarios = [f"{h:02d}:00" for h in range(6, 23)]  # 6h até 22h

        professor = self.object
        horarios_disponiveis = Horario.objects.filter(professor=professor, disponivel=True)

        agenda = {}
        for idx, dia in enumerate(dias):
            agenda[dias_labels[idx]] = {}
            for hora in horarios:
                existe = horarios_disponiveis.filter(data=dia, hora=hora).exists()
                agenda[dias_labels[idx]][hora] = existe  # True se disponível, False se não

        context["dias"] = dias_labels
        context["horarios"] = horarios
        context["agenda"] = agenda
        return context
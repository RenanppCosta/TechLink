from django.views.generic.detail import DetailView
from accounts.models import PerfilProfessor
from datetime import datetime, timedelta

class ProfessorDetailView(DetailView):
    model = PerfilProfessor
    template_name = 'profiles/professor_detail.html'
    context_object_name = 'perfil_professor'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        dias_semana = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
        hoje = datetime.today()
        dias = []
        for i in range(7):
            data = hoje + timedelta(days=i)
            nome_dia = data.strftime('%a')  # 'Mon', 'Tue', ...
            # Mapeamento para pt-br curto
            nome_dia_pt = {
                'Mon': 'Seg',
                'Tue': 'Ter',
                'Wed': 'Qua',
                'Thu': 'Qui',
                'Fri': 'Sex',
                'Sat': 'Sáb',
                'Sun': 'Dom'
            }[nome_dia]
            dias.append(f"{nome_dia_pt} {data.day:02d}/{data.month:02d}")

        horarios = [f"{h}:00" for h in range(6, 23)]  # 6h até 22h

        agenda = {}
        for dia in dias:
            agenda[dia] = {}
            for hora in horarios:
                agenda[dia][hora] = "disponivel"  # ou "agendado", etc

        context["dias"] = dias
        context["horarios"] = horarios
        context["agenda"] = agenda
        return context
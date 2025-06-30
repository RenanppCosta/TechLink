from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from agendamentos.models import Horario
from datetime import datetime, timedelta, time
from accounts.forms import HorarioDisponivelForm

class HorarioProfessorView(LoginRequiredMixin, TemplateView):
    template_name = 'profiles/horario_professor.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.tipo == 'professor':
            context['form'] = HorarioDisponivelForm(professor=self.request.user.professor_profile)
        return context

    def post(self, request, *args, **kwargs):
        professor = request.user.professor_profile
        form = HorarioDisponivelForm(request.POST, professor=professor)
        if form.is_valid():
            Horario.objects.filter(professor=professor).update(disponivel=False)
            for field in form.fields:
                if form.cleaned_data.get(field):
                    dia_str, hora_str = field.split('|')
                    data = datetime.strptime(dia_str, "%Y-%m-%d").date()
                    horario, _ = Horario.objects.get_or_create(
                        professor=professor,
                        data=data,
                        hora=hora_str,
                        defaults={'disponivel': True}
                    )
                    horario.disponivel = True
                    horario.save()
            return redirect('accounts:self_user_profile')
        # Se não for válido, renderiza novamente com o form preenchido
        context = self.get_context_data()
        context['form'] = form
        return self.render_to_response(context)
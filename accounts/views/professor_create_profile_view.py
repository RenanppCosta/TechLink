from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from accounts.models import PerfilProfessor
from accounts.forms.professor_form import PerfilProfessorForm
from django.contrib.auth.mixins import LoginRequiredMixin

class ProfessorCreateProfileView(LoginRequiredMixin, CreateView):
    model = PerfilProfessor
    form_class = PerfilProfessorForm
    template_name = 'profiles/completar_perfil_professor.html'
    success_url = reverse_lazy('accounts:self_user_profile')

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        return super().form_valid(form)

from django.views import View
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import PerfilProfessor, Tema

class DeletaTemaView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        tema_id = kwargs.get('tema_id')
        usuario = request.user
        perfil_professor = get_object_or_404(PerfilProfessor, usuario=usuario)
        tema = get_object_or_404(Tema, id=tema_id)
        perfil_professor.temas.remove(tema)
        return redirect('accounts:self_user_profile')
from django.views.generic.detail import DetailView
from accounts.models import PerfilProfessor

class ProfessorDetailView(DetailView):
    model = PerfilProfessor
    template_name = 'profiles/professor_detail.html'
    context_object_name = 'perfil_professor'
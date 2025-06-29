from django.views.generic import ListView
from accounts.models import PerfilProfessor
from django.db.models import Q

class ProfessorSearchView(ListView):
    model = PerfilProfessor
    template_name = 'techlink/busca_professor.html'
    context_object_name = 'professores'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        return PerfilProfessor.objects.filter(
            Q(usuario__nome__icontains=query) |
            Q(temas__nome__icontains=query)
        ).distinct()
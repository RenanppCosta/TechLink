from django.views.generic import ListView
from accounts.models import PerfilProfessor
from django.db.models import Q

class ProfessorSearchView(ListView):
    model = PerfilProfessor
    template_name = 'techlink/busca_professor.html'
    context_object_name = 'professores'

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        ordenar = self.request.GET.get('ordenar')

        qs = PerfilProfessor.objects.all()

        if query:
            qs = qs.filter(
                Q(usuario__nome__icontains=query) |
                Q(usuario__sobrenome__icontains=query) |
                Q(temas__nome__icontains=query)
            ).distinct()

        if ordenar == 'asc':
            qs = qs.order_by('usuario__nome')
        elif ordenar == 'desc':
            qs = qs.order_by('-usuario__nome')

        return qs
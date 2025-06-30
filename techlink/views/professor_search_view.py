# Em seu arquivo views.py
from django.db.models import Count 
from django.views.generic import ListView
from accounts.models import PerfilProfessor
from django.db.models import Q

class ProfessorSearchView(ListView):
    model = PerfilProfessor
    template_name = 'techlink/busca_professor.html'
    context_object_name = 'professores'

    def get_queryset(self):
        """
        Este método agora retorna a LISTA COMPLETA de professores
        que correspondem à busca e ordenação.
        """
        query = self.request.GET.get('q', '').strip()
        ordenar = self.request.GET.get('ordenar')

        qs = PerfilProfessor.objects.select_related('usuario').annotate(quantidade_aulas=Count('aulas' , distinct=True)).prefetch_related('temas').all()

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
        elif ordenar == 'popular':
            qs = qs.order_by('-quantidade_aulas')

        return qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        query = self.request.GET.get('q', '').strip()
        context['search_query'] = query

        if query:
            context['professores_destacados'] = self.object_list.order_by('-quantidade_aulas')[:6]
        else:
            context['professores_destacados'] = professores = PerfilProfessor.objects.select_related('usuario').annotate(
            quantidade_aulas=Count('aulas', distinct=True) 
        ).order_by('-quantidade_aulas')[:6]

        return context
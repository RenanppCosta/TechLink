from django.shortcuts import render
from django.views import View
from django.db.models import Q
from accounts.models import PerfilProfessor

class HomeView(View):
    template_name = 'techlink/base.html'
    def get(self, request):
        return render(request, self.template_name)

class ProfessorSearchView(View):
    template_name = 'techlink/professor_search.html'

    def get(self, request):
        query = request.GET.get('q', '')
        professores = []
        if query:
            professores = PerfilProfessor.objects.filter(
                Q(usuario__nome__icontains=query) |
                Q(areas_conhecimento__icontains=query)
            )
        return render(request, self.template_name, {'professores': professores, 'query': query})
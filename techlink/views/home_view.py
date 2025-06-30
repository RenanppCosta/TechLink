from django.shortcuts import render
from django.views import View
from django.db.models import Count 
from accounts.models import PerfilProfessor

class HomePageView(View):
    template_name = 'techlink/home.html'

    def get(self, request):
        professores = PerfilProfessor.objects.select_related('usuario').annotate(
            quantidade_aulas=Count('aulas', distinct=True) 
        ).order_by('-quantidade_aulas')[:5]
        
        context = {
            'professores': professores
        }
        
        return render(request, self.template_name, context)
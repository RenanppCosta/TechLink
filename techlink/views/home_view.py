from django.shortcuts import render
from django.views import View
from accounts.models import PerfilProfessor
# A importação de Q não é necessária para esta view
# from django.db.models import Q


class HomePageView(View):
    template_name = 'techlink/home.html'

    def get(self, request):
        # 1. Busque os dados dentro do método get
        professores = PerfilProfessor.objects.select_related('usuario').all()[:5]
        
        # 2. Crie o dicionário de contexto aqui
        context = {
            'professores': professores
        }
        
        # 3. Passe o contexto para a função render
        return render(request, self.template_name, context)
from django.shortcuts import render
from django.views import View
from django.db.models import Q
from accounts.models import PerfilProfessor


class HomePageView(View):
    template_name = 'techlink/home.html'
    context = {
        'professores': PerfilProfessor.objects.select_related('usuario').all()[:6]
    }

    def get(self, request):
        return render(request, self.template_name)

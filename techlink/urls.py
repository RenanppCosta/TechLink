from django.urls import path
from techlink.views import HomeView, ProfessorSearchView


app_name = 'techlink'

urlpatterns = [
    path('home/', HomeView.as_view(), name='home'),
    path('buscar/', ProfessorSearchView.as_view(), name='buscar')

]
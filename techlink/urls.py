from django.urls import path
from techlink.views import ProfessorSearchView,HomePageView

app_name = 'techlink'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('buscar/', ProfessorSearchView.as_view(), name='buscar'),
]

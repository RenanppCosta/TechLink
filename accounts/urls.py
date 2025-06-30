from django.urls import path
from django.contrib.auth.views import LogoutView
from accounts.views import(
    LoginView,
    RegisterView,
    UserProfileEditView,
    ProfessorDetailView,
    DeletaTemaView,
    logout_view,
    HorarioProfessorView
)
from accounts.models import CustomUser

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('registrar/', RegisterView.as_view(), name='register'),
    path('seu-perfil', UserProfileEditView.as_view(), name='self_user_profile'),
    path('professor/<int:pk>', ProfessorDetailView.as_view(), name='professor_detail'),
    path('tema/delete/<int:tema_id>/', DeletaTemaView.as_view(), name='delete_tema'),
    path('professor/horarios/', HorarioProfessorView.as_view(), name='horario_professor'),
]
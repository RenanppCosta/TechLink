from django.urls import path
from django.contrib.auth.views import LogoutView
from accounts.views import(
    LoginView,
    RegisterView,
    UserProfileEditView,
    ProfessorCreateProfileView
)
from accounts.models import CustomUser

app_name = 'accounts'

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='accounts:login'), name='logout'),
    path('registrar/', RegisterView.as_view(), name='register'),
    path('usuario/me', UserProfileEditView.as_view(), name='self_user_profile'),
    path('usuario/<int:pk>', UserProfileEditView.as_view(), name='other_ser_profile'),
    path('completar-perfil-professor/', ProfessorCreateProfileView.as_view(), name='completar_perfil_professor'),
]
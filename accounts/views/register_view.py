from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from django.contrib.auth import login
from accounts.forms import CustomUserCreationForm
from accounts.models import PerfilProfessor

class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        user = form.save()

        if user.tipo == 'Professor':
            PerfilProfessor.objects.create(usuario=user)

        return super().form_valid(form)

from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from accounts.forms import CustomUserCreationForm

class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
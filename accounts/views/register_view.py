from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from accounts.forms import CustomUserCreationForm, PerfilProfessorForm

class RegisterView(FormView):
    template_name = 'accounts/register.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['profile_form'] = CustomUserCreationForm()
        context['professor_form'] = PerfilProfessorForm()
        return context

    def post(self, request, *args, **kwargs):
        user_form = CustomUserCreationForm(request.POST)
        professor_form = PerfilProfessorForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            if user.tipo == 'professor' and professor_form.is_valid():
                professor_form.save(usuario=user)
            return redirect(self.success_url)
        return render(request, self.template_name, {
            'profile_form': user_form,
            'professor_form': professor_form
        })
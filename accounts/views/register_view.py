from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from accounts.forms import CustomUserCreationForm, PerfilProfessorForm
from accounts.models import Tema
from accounts.models.perfil_aluno import PerfilAluno

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
        profile_form = CustomUserCreationForm(request.POST)
        professor_form = PerfilProfessorForm(request.POST)
        temas_digitados = request.POST.getlist('temas[]')

        if profile_form.is_valid():
            user = profile_form.save()
            print("Usuário criado:", user, user.tipo)
            if user.tipo == 'professor':
                print("Dados do professor:", request.POST)
                print("Professor form válido?", professor_form.is_valid())
                print("Erros do professor_form:", professor_form.errors)
                if professor_form.is_valid():
                    perfil_professor = professor_form.save(commit=False)
                    perfil_professor.usuario = user
                    perfil_professor.save()
                    temas_objs = []
                    for nome in temas_digitados:
                        nome = nome.strip()
                        if nome:
                            tema, _ = Tema.objects.get_or_create(nome=nome)
                            temas_objs.append(tema)
                    perfil_professor.temas.set(temas_objs)
            elif user.tipo == 'aluno':
                PerfilAluno.objects.create(usuario=user)
            return redirect(self.success_url)
        return render(request, self.template_name, {
            'profile_form': profile_form,
            'professor_form': professor_form
        })
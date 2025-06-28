from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from accounts.models import PerfilProfessor
from accounts.forms.user_form import CustomPasswordChangeForm, CustomUserCreationForm, UserProfileUpdateForm
from accounts.forms.professor_form import PerfilProfessorForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

class UserProfileEditView(LoginRequiredMixin, TemplateView):
    template_name = ''

    def get_template_names(self):
        usuario = self.request.user
        if usuario.tipo == 'professor':
            return ['profiles/perfil_professor.html']
        elif usuario.tipo == 'aluno':
            return ['profiles/perfil_aluno.html']
        return ['profiles/perfil_usuario.html']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        usuario = self.request.user

        context['usuario'] = usuario
        context['profile_form'] = UserProfileUpdateForm(instance=usuario)
        context['password_form'] = CustomPasswordChangeForm(user=usuario)

        if usuario.tipo == 'professor':
            perfil_professor, created = PerfilProfessor.objects.get_or_create(usuario=usuario)
            context['professor_form'] = PerfilProfessorForm(instance=perfil_professor)

        return context


    def post(self, request, *args, **kwargs):
        usuario = request.user

        if 'submit_perfil' in request.POST:
            profile_form = UserProfileUpdateForm(request.POST, request.FILES, instance=request.user)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('accounts:self_user_profile')

            context = self.get_context_data()
            context['profile_form'] = profile_form
            return self.render_to_response(context)

        elif 'submit_professor' in request.POST and usuario.tipo == 'professor':
            perfil_professor, created = PerfilProfessor.objects.get_or_create(usuario=usuario)
            professor_form = PerfilProfessorForm(request.POST, instance=perfil_professor)
            if professor_form.is_valid():
                professor_form.save()
                return redirect('accounts:self_user_profile')

            context = self.get_context_data()
            context['professor_form'] = professor_form
            return self.render_to_response(context)
             
        elif 'submit_senha' in request.POST:
            password_form = PasswordChangeForm(user=usuario, data=request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                return redirect('accounts:user_profile')

            context = self.get_context_data()
            context['password_form'] = password_form
            return self.render_to_response(context)
        
        
        

        return redirect('accounts:self_user_profile')

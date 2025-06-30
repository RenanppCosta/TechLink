from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from accounts.models import PerfilProfessor
from accounts.forms.user_form import CustomPasswordChangeForm, CustomUserCreationForm, UserProfileUpdateForm
from accounts.forms import PerfilProfessorForm, HorarioDisponivelForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from agendamentos.models import Horario
from datetime import datetime
from agendamentos.models import Aula

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
            context['form'] = HorarioDisponivelForm(professor=perfil_professor)
            context['aulas_agendadas'] = Aula.objects.filter(professor=perfil_professor).select_related('aluno', 'horario')

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
            temas_digitados = request.POST.getlist('temas[]')  

            if professor_form.is_valid():
                perfil = professor_form.save(commit=False)
                from accounts.models import Tema
                temas_objs = []
                for nome in temas_digitados:
                    nome = nome.strip()
                    if nome:
                        tema, _ = Tema.objects.get_or_create(nome=nome)
                        temas_objs.append(tema)
                perfil.save()

                # Remover temas marcados para remoção
                remover_temas = request.POST.getlist('remover_temas[]')
                if remover_temas:
                    perfil.temas.remove(*remover_temas)

                # Adicionar novos temas
                for tema in temas_objs:
                    if not perfil.temas.filter(pk=tema.pk).exists():
                        perfil.temas.add(tema)
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
        
        elif 'submit_horarios' in request.POST and usuario.tipo == 'professor':
            perfil_professor, created = PerfilProfessor.objects.get_or_create(usuario=usuario)
            form = HorarioDisponivelForm(request.POST, professor=perfil_professor)
            if form.is_valid():
                Horario.objects.filter(professor=perfil_professor).update(disponivel=False)
                for field in form.fields:
                    if form.cleaned_data.get(field):
                        dia_str, hora_str = field.split('|')
                        data = datetime.strptime(dia_str, "%Y-%m-%d").date()
                        horario, _ = Horario.objects.get_or_create(
                            professor=perfil_professor,
                            data=data,
                            hora=hora_str,
                            defaults={'disponivel': True}
                        )
                        horario.disponivel = True
                        horario.save()
                return redirect('accounts:self_user_profile')
            context = self.get_context_data()
            context['form'] = form
            return self.render_to_response(context)
        
        
        

        return redirect('accounts:self_user_profile')

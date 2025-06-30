from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, PerfilProfessor, Tema, PerfilAluno
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

class CustomUserCreationAdminForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'nome', 'sobrenome', 'tipo')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

class CustomUserChangeAdminForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser
        fields = ('email', 'nome', 'sobrenome', 'tipo', 'password', 'is_active', 'is_staff', 'is_superuser')

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationAdminForm
    form = CustomUserChangeAdminForm
    model = CustomUser
    list_display = ('email', 'nome', 'sobrenome', 'tipo', 'is_staff', 'is_active')
    list_filter = ('tipo', 'is_staff', 'is_active')
    search_fields = ('email', 'nome', 'sobrenome')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'nome', 'sobrenome', 'num_celular', 'tipo', 'foto_perfil')}),
        ('Permissões', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas', {'fields': ('last_login', 'data_criacao')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nome', 'sobrenome', 'tipo', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )

class PerfilAlunoAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario',)
    search_fields = ('usuario__nome', 'usuario__email')
    raw_id_fields = ('usuario',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(PerfilProfessor)
admin.site.register(Tema)
admin.site.register(PerfilAluno, PerfilAlunoAdmin)
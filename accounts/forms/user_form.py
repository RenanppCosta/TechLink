from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import PasswordChangeForm
from accounts.models import CustomUser

# accounts/forms.py
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.forms import PasswordChangeForm
from accounts.models import CustomUser

class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Senha', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ['email', 'nome', 'sobrenome', 'num_celular', 'tipo']
        widgets = {
            'telefone': forms.TextInput(attrs={
                'placeholder': 'Ex: (21) 98765-4321'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

       
        tailwind_classes = 'w-full px-4 py-2 text-gray-700 bg-white border border-gray-200 outline-none'

   
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': tailwind_classes})


        self.fields['nome'].widget.attrs.update({'placeholder': 'Primeiro nome'})
        self.fields['sobrenome'].widget.attrs.update({'placeholder': 'Último nome'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['num_celular'].widget.attrs.update({'placeholder': 'Telefone'})
        self.fields['password1'].widget.attrs.update({'placeholder': '••••••••'})
        self.fields['password2'].widget.attrs.update({'placeholder': '••••••••'})


    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("As senhas não coincidem.")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserProfileUpdateForm(forms.ModelForm):
    """
    Formulário para o usuário editar suas próprias informações de perfil.
    """
    class Meta:
        model = CustomUser
        fields = ['foto_perfil', 'nome', 'sobrenome', 'email', 'num_celular']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplica as classes de estilo Tailwind que você quer em todos os campos
        tailwind_classes = 'w-full px-4 py-2 mt-2 text-gray-500 bg-white border border-gray-200 mb-5 outline-none'
        
        for field_name, field in self.fields.items():
            # O campo de arquivo (profile_picture) pode ter um estilo diferente
            if isinstance(field.widget, forms.FileInput):
                field.widget.attrs.update({'class': 'w-full text-sm text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-red-50 file:text-red-700 hover:file:bg-red-100'})
            else:
                field.widget.attrs.update({'class': tailwind_classes})


class CustomAuthenticationForm(forms.Form):
    email = forms.EmailField(label="Email",
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-200 mb-5 outline-none',
            'placeholder': 'Email'
        })
    )
    password = forms.CharField(label="Senha", 
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-2 mt-2 text-gray-700 bg-white border border-gray-200 mb-7 outline-none',
            'placeholder': 'Senha'
        })
    )

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Adiciona as classes do Tailwind a cada um dos campos
        self.fields['old_password'].widget.attrs.update({
            'class': 'w-full px-4 py-2 mt-2 text-gray-500 bg-white border border-gray-200 mb-5 outline-none',
            'placeholder': '••••••••'
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'w-full px-4 py-2 mt-2 text-gray-500 bg-white border border-gray-200 mb-5 outline-none',
            'placeholder': '••••••••'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'w-full px-4 py-2 mt-2 text-gray-500 bg-white border border-gray-200 mb-5 outline-none',
            'placeholder': '••••••••'
        })
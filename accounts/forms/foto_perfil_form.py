from django import forms
from accounts.models import CustomUser

class FotoPerfilForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['foto_perfil']
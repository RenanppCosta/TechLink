from django import forms
from accounts.models import Tema

class TemaForm(forms.ModelForm):
    class Meta:
        model = Tema
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded',
                'placeholder': 'Digite o nome do tema'
            }),
        }
from django import forms
from accounts.models import PerfilProfessor

class PerfilProfessorForm(forms.ModelForm):
    class Meta:
        model = PerfilProfessor
        fields = ['apresentacao', 'valor_hora']
        widgets = {
            'apresentacao': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 text-gray-700 bg-white border border-gray-200 outline-none',
                'placeholder': 'Fale um pouco sobre você e sua área de atuação...',
                'rows': 4
            }),
            'valor_hora': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-2 text-gray-700 bg-white border border-gray-200 outline-none',
                'placeholder': 'Valor da hora/aula'
            }),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['apresentacao'].required = False
            self.fields['valor_hora'].required = False
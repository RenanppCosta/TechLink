from django import forms
from accounts.models import PerfilProfessor

class PerfilProfessorForm(forms.ModelForm):
    class Meta:
        model = PerfilProfessor
        fields = ['formacao', 'apresentacao', 'valor_hora', 'areas_conhecimento']
        

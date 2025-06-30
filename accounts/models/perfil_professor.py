from django.db import models
from .custom_user import CustomUser
from .tema import Tema


class PerfilProfessor(models.Model):
    usuario = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='professor_profile')
    apresentacao = models.TextField(blank=True, null=True)
    valor_hora = models.DecimalField(max_digits=6, decimal_places=2, default=0.00,blank=True, null=True)
    temas = models.ManyToManyField(Tema, related_name='temas_professor')

    def __str__(self):
        return self.usuario.nome

from django.db import models
from .horario import Horario

class Aula(models.Model):
    STATUS_CHOICES = [
        ('agendada', 'Agendada'),
        ('realizada', 'Realizada'),
        ('cancelada', 'Cancelada'),
    ]

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='agendada')
    horario = models.OneToOneField(Horario, on_delete=models.CASCADE, related_name='aula')
    aluno = models.ForeignKey('accounts.PerfilAluno', on_delete=models.CASCADE, related_name='aulas')
    professor = models.ForeignKey('accounts.PerfilProfessor', on_delete=models.CASCADE, related_name='aulas')
    pago = models.BooleanField(default=False)
    criado_em = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Aula de {self.aluno} com {self.professor} em {self.horario.data} {self.horario.hora}"
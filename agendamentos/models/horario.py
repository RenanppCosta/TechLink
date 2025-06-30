from django.db import models
from accounts.models import PerfilProfessor

class Horario(models.Model):
    professor = models.ForeignKey(PerfilProfessor, on_delete=models.CASCADE, related_name='agendamentos')
    data = models.DateField()
    hora = models.TimeField()
    disponivel = models.BooleanField(default=True)

    class Meta:
        unique_together = ('professor', 'data', 'hora')

    def __str__(self):
        return f"{self.professor} - {self.data} {self.hora} ({'Disponível' if self.disponivel else 'Indisponível'})"

from django.db import models
from django.conf import settings

class Pagamento(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('pago', 'Pago'),
        ('falhou', 'Falhou'),
        ('reembolsado', 'Reembolsado'),
    ]
    
    aluno = models.ForeignKey('accounts.PerfilAluno', on_delete=models.PROTECT, related_name='pagamentos')
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    
    # Guarda o ID da transação do provedor (Stripe, AbacatePay, etc.)
    id_transacao_provedor = models.CharField(max_length=255, unique=True, null=True, blank=True)
    metodo_pagamento = models.CharField(max_length=50, null=True, blank=True) # ex: 'card', 'pix'
    
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Pagamento {self.id} de {self.aluno} - R$ {self.valor} ({self.status})"


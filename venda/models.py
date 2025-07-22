from django.db import models
from django.contrib.auth.models import User
from produto.models import Produto
from clientes.models import Cliente

class Venda(models.Model):
    STATUS_CHOICES = [
        ('PENDENTE', 'Pendente'),
        ('APROVADO', 'Aprovado'),
        ('PROGRAMADO', 'Programado'),
        ('PROCESSADO', 'Processado'),
        ('CANCELADO', 'Cancelado'),
    ]
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    data_venda = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDENTE')
    data_entrega = models.DateField(null=True, blank=True)
    gerente_responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    observacoes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Venda #{self.id} - {self.cliente.nome} - {self.produto.nome} - {self.status}"

    @property
    def valor_total(self):
        return self.quantidade * self.produto.preco

from django.db import models
from produto.models import Produto
from clientes.models import Cliente

class Venda(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)
    data_venda = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Venda #{self.id} - {self.cliente.nome} - {self.produto.nome}"

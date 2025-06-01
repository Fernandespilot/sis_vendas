from django.db import models

class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.nome

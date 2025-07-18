from django.db import models


class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    telefone = models.CharField(max_length=20, blank=True)
    cnpj = models.CharField(max_length=18, blank=True)
    ie = models.CharField("Inscrição Estadual", max_length=20, blank=True)
    endereco = models.CharField(max_length=255, blank=True)
    municipio = models.CharField(max_length=100, blank=True)
    uf = models.CharField(max_length=2, blank=True)

    def __str__(self):
        return self.nome

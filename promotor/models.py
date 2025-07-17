from django.contrib.auth.models import User
from django.db import models


class Promotor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    municipios_cobertos = models.TextField(help_text="Informe os municípios cobertos separados por vírgula.")

    def __str__(self):
        return self.nome



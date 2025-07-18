from django.contrib import admin
from .models import Cliente

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('nome', 'email', 'telefone', 'cnpj', 'ie', 'municipio', 'uf')
    search_fields = ('nome', 'email', 'cnpj', 'municipio', 'uf')

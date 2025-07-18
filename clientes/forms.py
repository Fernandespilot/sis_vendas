from django import forms
from .models import Cliente

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nome', 'email', 'telefone', 'cnpj', 'ie', 'endereco', 'municipio', 'uf']
        labels = {
            'nome': 'Nome',
            'email': 'Email',
            'telefone': 'Telefone',
            'cnpj': 'CNPJ',
            'ie': 'Inscrição Estadual',
            'endereco': 'Endereço',
            'municipio': 'Município',
            'uf': 'UF',
        }

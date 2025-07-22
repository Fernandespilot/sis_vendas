from django import forms
from .models import Promotor

class PromotorForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput, label="Senha")
    class Meta:
        model = Promotor
        fields = ['nome', 'email', 'municipios_cobertos']
        widgets = {
            'municipios_cobertos': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Ex: Cidade1, Cidade2, Cidade3'})
        }

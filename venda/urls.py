from django.urls import path
from .views import lista_vendas

urlpatterns = [
    path('venda/', lista_vendas, name='lista_vendas'),
]

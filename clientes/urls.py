from django.urls import path
from .views import lista_clientes, cadastrar_cliente, editar_cliente, excluir_cliente

urlpatterns = [
    path('clientes/', lista_clientes, name='lista_clientes'),
    path('clientes/cadastrar/', cadastrar_cliente, name='cadastrar_cliente'),
    path('clientes/<int:pk>/editar/', editar_cliente, name='editar_cliente'),
    path('clientes/<int:pk>/excluir/', excluir_cliente, name='excluir_cliente'),
]

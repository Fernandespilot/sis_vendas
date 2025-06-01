from django.urls import path
from . import views

urlpatterns = [
    path('cadastrar/', views.cadastrar_produto, name='cadastrar_produto'),
    path('<int:id>/editar/', views.editar_produto, name='editar_produto'),
    path('<int:id>/excluir/', views.excluir_produto, name='excluir_produto'),
    path('', views.lista_produtos, name='lista_produtos'),
]

from django.urls import path
from .views import cadastrar_promotor, lista_promotores, editar_promotor, visualizar_promotor, excluir_promotor

urlpatterns = [
    path('', lista_promotores, name='lista_promotores'),
    path('cadastrar/', cadastrar_promotor, name='cadastrar_promotor'),
    path('editar/<int:pk>/', editar_promotor, name='editar_promotor'),
    path('visualizar/<int:pk>/', visualizar_promotor, name='visualizar_promotor'),
    path('excluir/<int:pk>/', excluir_promotor, name='excluir_promotor'),
]

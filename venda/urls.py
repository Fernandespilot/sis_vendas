from django.urls import path
from .views import (
    lista_vendas, pedidos_aprovados, programar_entrega, 
    entregas_hoje, processar_entrega, relatorios_produtos,
    relatorio_estoque_baixo, relatorio_promocao, relatorio_por_grupo,
    exportar_relatorio_pdf, exportar_relatorio_excel
)

urlpatterns = [
    path('venda/', lista_vendas, name='lista_vendas'),
    
    # US7 - Programar entrega
    path('pedidos-aprovados/', pedidos_aprovados, name='pedidos_aprovados'),
    path('programar-entrega/<int:venda_id>/', programar_entrega, name='programar_entrega'),
    
    # US8 - Processar entrega
    path('entregas-hoje/', entregas_hoje, name='entregas_hoje'),
    path('processar-entrega/<int:venda_id>/', processar_entrega, name='processar_entrega'),
    
    # US9 - Relatórios
    path('relatorios/', relatorios_produtos, name='relatorios_produtos'),
    path('relatorio/estoque-baixo/', relatorio_estoque_baixo, name='relatorio_estoque_baixo'),
    path('relatorio/promocao/', relatorio_promocao, name='relatorio_promocao'),
    path('relatorio/por-grupo/', relatorio_por_grupo, name='relatorio_por_grupo'),
    path('relatorio/pdf/<str:tipo>/', exportar_relatorio_pdf, name='exportar_relatorio_pdf'),
    path('relatorio/excel/<str:tipo>/', exportar_relatorio_excel, name='exportar_relatorio_excel'),
]

import matplotlib.pyplot as plt
import numpy as np
import os
from datetime import date

# Configurações visuais
plt.style.use('ggplot')
cores = ['#4CAF50', '#F44336', '#2196F3', '#FF9800', '#9C27B0']
fonte_titulo = {'fontname': 'Arial', 'fontsize': 14, 'fontweight': 'bold'}
fonte_labels = {'fontname': 'Arial', 'fontsize': 10}

def criar_diretorio_output():
    """Criar diretório para os gráficos se não existir"""
    if not os.path.exists('output'):
        os.makedirs('output')

def grafico_pizza_status_testes():
    """Gráfico de pizza mostrando status dos testes"""
    aprovados = 7
    reprovados = 5
    
    # Criar figura
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Dados
    labels = ['Aprovados', 'Reprovados']
    tamanhos = [aprovados, reprovados]
    explode = (0.1, 0)  # Destacar fatia dos aprovados
    
    # Criar gráfico
    wedges, texts, autotexts = ax.pie(
        tamanhos, 
        explode=explode, 
        labels=labels, 
        autopct='%1.1f%%',
        colors=[cores[0], cores[1]], 
        shadow=True, 
        startangle=90
    )
    
    # Estilizar textos
    for text in texts:
        text.set_fontsize(12)
    for autotext in autotexts:
        autotext.set_fontsize(12)
        autotext.set_fontweight('bold')
    
    # Adicionar título
    ax.set_title('Status dos Testes Automatizados', **fonte_titulo)
    
    # Salvar figura
    plt.tight_layout()
    plt.savefig('output/status_testes.png', dpi=300)
    print(f"✅ Gráfico de status dos testes salvo em 'output/status_testes.png'")

def grafico_barras_cobertura_codigo():
    """Gráfico de barras para cobertura de código"""
    # Criar figura
    fig, ax = plt.subplots(figsize=(8, 6))
    
    # Dados
    componentes = ['Backend', 'Frontend']
    cobertura = [100, 0]
    posicoes = np.arange(len(componentes))
    cores_barras = [cores[0], cores[1]]
    
    # Criar barras
    barras = ax.bar(posicoes, cobertura, color=cores_barras, width=0.5)
    
    # Adicionar texto nas barras
    for i, valor in enumerate(cobertura):
        ax.text(i, valor/2, f"{valor}%", ha='center', va='center', 
                fontweight='bold', color='white', fontsize=14)
    
    # Configuração do eixo Y
    ax.set_ylim(0, 110)
    ax.set_yticks(range(0, 101, 20))
    ax.set_yticklabels([f'{i}%' for i in range(0, 101, 20)])
    
    # Título e labels
    ax.set_title('Cobertura de Código por Componente', **fonte_titulo)
    ax.set_ylabel('Cobertura (%)', **fonte_labels)
    ax.set_xticks(posicoes)
    ax.set_xticklabels(componentes, **fonte_labels)
    
    # Salvar figura
    plt.tight_layout()
    plt.savefig('output/cobertura_codigo.png', dpi=300)
    print(f"✅ Gráfico de cobertura de código salvo em 'output/cobertura_codigo.png'")

def grafico_barras_funcionalidades():
    """Gráfico de barras das funcionalidades por user story"""
    # Criar figura
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Dados
    user_stories = ['US7', 'US8', 'US9']
    backend = [100, 100, 100]
    frontend = [0, 0, 0]
    exportacao = [0, 0, 100]
    
    # Posições
    x = np.arange(len(user_stories))
    largura = 0.25
    
    # Criar barras
    ax.bar(x - largura, backend, largura, label='Backend', color=cores[0])
    ax.bar(x, frontend, largura, label='Frontend', color=cores[1])
    ax.bar(x + largura, exportacao, largura, label='Exportação', color=cores[2])
    
    # Configuração dos eixos
    ax.set_title('Implementação por User Story e Componente (%)', **fonte_titulo)
    ax.set_ylabel('Percentual Concluído (%)', **fonte_labels)
    ax.set_xticks(x)
    ax.set_xticklabels(user_stories)
    ax.set_yticks(range(0, 101, 20))
    ax.set_yticklabels([f'{i}%' for i in range(0, 101, 20)])
    ax.legend()
    
    # Salvar figura
    plt.tight_layout()
    plt.savefig('output/funcionalidades_user_story.png', dpi=300)
    print(f"✅ Gráfico de funcionalidades por user story salvo em 'output/funcionalidades_user_story.png'")

def grafico_tempo_estimado():
    """Gráfico de tempo estimado para conclusão"""
    # Criar figura
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Dados
    categorias = ['Implementação\nTemplates', 'Testes\nValidação', 'Deploy\nFinal', 'Total']
    tempos = [2.5, 1, 0.5, 4]
    
    # Criar barras horizontais
    barras = ax.barh(categorias, tempos, color=[cores[0], cores[2], cores[3], cores[4]])
    
    # Adicionar valores nas barras
    for i, barra in enumerate(barras):
        width = barra.get_width()
        label = f"{tempos[i]} dias" if i < 3 else f"{tempos[i]} dias úteis"
        ax.text(width/2, barra.get_y() + barra.get_height()/2,
                label, ha='center', va='center', color='white', fontweight='bold')
    
    # Configuração dos eixos
    ax.set_title('Tempo Estimado para Conclusão', **fonte_titulo)
    ax.set_xlabel('Dias Úteis', **fonte_labels)
    ax.set_xlim(0, 5)
    ax.invert_yaxis()  # Para que "Total" fique embaixo
    
    # Salvar figura
    plt.tight_layout()
    plt.savefig('output/tempo_estimado.png', dpi=300)
    print(f"✅ Gráfico de tempo estimado salvo em 'output/tempo_estimado.png'")

def grafico_resumo_status():
    """Tabela resumo do status das user stories"""
    # Criar figura
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Remover eixos
    ax.axis('tight')
    ax.axis('off')
    
    # Dados da tabela
    dados = [
        ['US7', 'Programar Entrega', 'PARCIAL', '100%', '0%', 'Templates Ausentes'],
        ['US8', 'Processar Entrega', 'PARCIAL', '100%', '0%', 'Templates Ausentes'],
        ['US9', 'Relatórios', 'PARCIAL', '100%', '0%', 'Templates Ausentes'],
    ]
    
    # Cabeçalhos
    colunas = ['User Story', 'Descrição', 'Status', 'Backend', 'Frontend', 'Observações']
    
    # Cores para o status
    cores_celulas = [
        ['white', 'white', '#FFC107', '#4CAF50', '#F44336', 'white'],
        ['white', 'white', '#FFC107', '#4CAF50', '#F44336', 'white'],
        ['white', 'white', '#FFC107', '#4CAF50', '#F44336', 'white']
    ]
    
    # Criar tabela
    tabela = ax.table(
        cellText=dados,
        colLabels=colunas,
        loc='center',
        cellLoc='center',
        cellColours=cores_celulas
    )
    
    # Estilizar tabela
    tabela.auto_set_font_size(False)
    tabela.set_fontsize(11)
    tabela.scale(1, 1.5)  # Ajustar altura das linhas
    
    # Para cabeçalhos
    for i in range(len(colunas)):
        tabela[(0, i)].set_fontsize(12)
        tabela[(0, i)].set_text_props(fontweight='bold')
        tabela[(0, i)].set_facecolor('#E0E0E0')
    
    # Título da figura
    plt.title('Status das User Stories', **fonte_titulo, pad=20)
    
    # Salvar figura
    plt.tight_layout()
    plt.savefig('output/resumo_status.png', dpi=300)
    print(f"✅ Tabela de resumo salva em 'output/resumo_status.png'")

def criar_relatorio_visual():
    """Criar todos os gráficos para o relatório"""
    print("\n🚀 Gerando gráficos para o relatório executivo...")
    criar_diretorio_output()
    
    # Gerar gráficos
    grafico_pizza_status_testes()
    grafico_barras_cobertura_codigo()
    grafico_barras_funcionalidades()
    grafico_tempo_estimado()
    grafico_resumo_status()
    
    print("\n✅ Todos os gráficos foram gerados na pasta 'output/'!")
    print("📊 Utilize-os para complementar o relatório executivo RELATORIO_EXECUTIVO.md")

# Executar a criação dos gráficos
if __name__ == "__main__":
    criar_relatorio_visual()

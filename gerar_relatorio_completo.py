#!/usr/bin/env python
"""
Script para gerar relatório completo de testes
Sistema de Vendas - Funcionalidades do Gerente de Estoque
"""

import os
import sys
import subprocess
import platform
from datetime import datetime

def print_header(mensagem):
    """Imprime cabeçalho formatado"""
    print("\n" + "=" * 80)
    print(f" {mensagem} ".center(80, "="))
    print("=" * 80)

def executar_comando(comando, descricao=None):
    """Executa um comando e exibe sua saída"""
    if descricao:
        print(f"\n🔄 {descricao}...")
    
    try:
        resultado = subprocess.run(comando, check=True, capture_output=True, text=True)
        if resultado.stdout:
            print(resultado.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao executar o comando: {e}")
        if e.stdout:
            print(e.stdout)
        if e.stderr:
            print(e.stderr)
        return False

def verificar_ambiente_virtual():
    """Verifica se estamos em um ambiente virtual"""
    return (hasattr(sys, 'real_prefix') or 
            (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix))

def ativar_ambiente():
    """Ativa o ambiente virtual ou orienta o usuário"""
    print_header("VERIFICANDO AMBIENTE")
    
    if verificar_ambiente_virtual():
        print("✅ Ambiente virtual ativo!")
        return True
    else:
        print("❌ Ambiente virtual não ativado!")
        
        venv_path = os.path.join(os.getcwd(), "venv_teste")
        if os.path.exists(venv_path):
            if platform.system() == "Windows":
                print("\nPara ativar o ambiente, execute no PowerShell:")
                print(f"   .\\venv_teste\\Scripts\\Activate.ps1")
                print("\nOu no cmd:")
                print(f"   .\\venv_teste\\Scripts\\activate.bat")
            else:
                print("\nPara ativar o ambiente, execute:")
                print(f"   source {venv_path}/bin/activate")
        else:
            print("\nAmbiente virtual não encontrado. Execute primeiro:")
            print("   python configurar_ambiente_teste.py")
        
        print("\nDepois execute novamente este script.")
        return False

def executar_testes():
    """Executa os testes automatizados"""
    print_header("EXECUTANDO TESTES AUTOMATIZADOS")
    
    # Primeiro, executar os testes simples
    print("\n📋 Executando testes simples...")
    if not executar_comando(["python", "teste_unitario_us789.py"], 
                           "Executando testes unitários"):
        return False
    
    # Executar os testes adicionais, se houver
    if os.path.exists("venda/tests_simplificados.py"):
        print("\n📋 Executando testes adicionais...")
        if not executar_comando(["python", "-c", "import os; os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sisvenda.settings'); import django; django.setup(); from venda.tests_simplificados import executar_testes; executar_testes()"],
                               "Executando testes adicionais"):
            return False
    
    return True

def gerar_graficos():
    """Gera os gráficos para o relatório"""
    print_header("GERANDO GRÁFICOS PARA O RELATÓRIO")
    
    return executar_comando(["python", "gerar_graficos_relatorio.py"],
                          "Gerando gráficos")

def gerar_cobertura():
    """Gera relatório de cobertura de código"""
    print_header("GERANDO RELATÓRIO DE COBERTURA DE CÓDIGO")
    
    # Executar os testes com coverage
    print("\n📊 Executando testes com coverage...")
    if not executar_comando(["coverage", "run", "--source=venda,produto", "teste_unitario_us789.py"],
                           "Executando testes com coverage"):
        return False
    
    # Gerar relatório de cobertura
    print("\n📊 Gerando relatório de cobertura...")
    if not executar_comando(["coverage", "report"],
                           "Gerando relatório de cobertura em texto"):
        return False
    
    # Gerar relatório HTML
    print("\n📊 Gerando relatório HTML de cobertura...")
    if not executar_comando(["coverage", "html"],
                           "Gerando relatório de cobertura em HTML"):
        return False
    
    print("\n✅ Relatório de cobertura gerado em: htmlcov/index.html")
    return True

def main():
    """Função principal"""
    print_header("GERADOR DE RELATÓRIO COMPLETO DE TESTES")
    print(f"Data/Hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("Sistema: SISVENDA - User Stories 7, 8 e 9")
    
    # Verificar ambiente virtual
    if not ativar_ambiente():
        return 1
    
    # Verificar dependências
    try:
        import matplotlib
        import numpy
        import coverage
    except ImportError:
        print("❌ Dependências não encontradas!")
        print("Execute primeiro: python configurar_ambiente_teste.py")
        return 1
    
    # Executar testes
    if not executar_testes():
        print("❌ Falha na execução dos testes!")
        return 1
    
    # Gerar gráficos
    if not gerar_graficos():
        print("❌ Falha na geração dos gráficos!")
        return 1
    
    # Gerar cobertura
    if not gerar_cobertura():
        print("❌ Falha na geração do relatório de cobertura!")
        return 1
    
    print_header("RELATÓRIO COMPLETO GERADO COM SUCESSO!")
    print("""
📄 Arquivos gerados:
- RELATORIO_EXECUTIVO.md - Relatório executivo resumido
- RELATORIO_TESTE_UNITARIO.md - Relatório técnico detalhado
- output/*.png - Gráficos para inclusão no relatório
- htmlcov/index.html - Relatório de cobertura de código

✅ Todos os arquivos estão prontos para serem incluídos na documentação!
""")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())

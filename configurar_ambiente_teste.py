#!/usr/bin/env python
"""
Configurador de Ambiente de Teste para SISVENDA
Automatiza a configuração do ambiente virtual e dependências para testes
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_header(mensagem):
    """Imprime cabeçalho formatado"""
    print("\n" + "=" * 80)
    print(f" {mensagem} ".center(80, "="))
    print("=" * 80)

def verificar_python():
    """Verifica a versão do Python"""
    print_header("Verificando versão do Python")
    
    versao = sys.version_info
    print(f"Python {versao.major}.{versao.minor}.{versao.micro}")
    
    if versao.major < 3 or (versao.major == 3 and versao.minor < 8):
        print("❌ ERRO: Versão do Python muito antiga!")
        print("Por favor, instale Python 3.8 ou superior.")
        sys.exit(1)
    else:
        print("✅ Versão do Python compatível!")

def criar_ambiente_virtual():
    """Cria e ativa o ambiente virtual para testes"""
    print_header("Configurando ambiente virtual")
    
    venv_path = Path("venv_teste")
    
    # Verificar se o ambiente virtual já existe
    if venv_path.exists():
        print("⚠️  Ambiente virtual já existe.")
        resposta = input("Deseja recriá-lo? (s/n): ").lower()
        if resposta == 's':
            print("🗑️  Removendo ambiente virtual existente...")
            try:
                if platform.system() == "Windows":
                    subprocess.run(["rmdir", "/S", "/Q", str(venv_path)], check=True)
                else:
                    subprocess.run(["rm", "-rf", str(venv_path)], check=True)
                print("✅ Ambiente virtual removido!")
            except subprocess.CalledProcessError:
                print("❌ Erro ao remover ambiente virtual.")
                return False
        else:
            print("ℹ️  Mantendo ambiente virtual existente.")
            return True
    
    # Criar ambiente virtual
    print("🔧 Criando novo ambiente virtual...")
    try:
        subprocess.run([sys.executable, "-m", "venv", str(venv_path)], check=True)
        print("✅ Ambiente virtual criado com sucesso!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao criar ambiente virtual.")
        return False

def instalar_dependencias(venv_path):
    """Instala as dependências necessárias para os testes"""
    print_header("Instalando dependências")
    
    # Determinar o caminho do pip no ambiente virtual
    if platform.system() == "Windows":
        pip_path = os.path.join(venv_path, "Scripts", "pip")
    else:
        pip_path = os.path.join(venv_path, "bin", "pip")
    
    # Atualizar pip
    print("📦 Atualizando pip...")
    try:
        subprocess.run([pip_path, "install", "--upgrade", "pip"], check=True)
    except subprocess.CalledProcessError:
        print("⚠️ Aviso: Não foi possível atualizar pip, continuando...")
    
    # Instalar Django
    print("\n📦 Instalando Django...")
    try:
        subprocess.run([pip_path, "install", "Django>=5.2,<6.0"], check=True)
        print("✅ Django instalado!")
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar Django.")
        return False
    
    # Instalar bibliotecas para relatórios
    print("\n📦 Instalando bibliotecas para relatórios...")
    try:
        subprocess.run([pip_path, "install", "reportlab", "openpyxl"], check=True)
        print("✅ Bibliotecas de relatório instaladas!")
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar bibliotecas de relatório.")
        return False
    
    # Instalar bibliotecas para gráficos do relatório
    print("\n📦 Instalando bibliotecas para gráficos...")
    try:
        subprocess.run([pip_path, "install", "matplotlib", "numpy"], check=True)
        print("✅ Bibliotecas de gráficos instaladas!")
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar bibliotecas de gráficos.")
        return False
    
    # Instalar cobertura de código
    print("\n📦 Instalando biblioteca de cobertura de código...")
    try:
        subprocess.run([pip_path, "install", "coverage"], check=True)
        print("✅ Coverage instalado!")
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar coverage.")
        return False
    
    return True

def configurar_ambiente():
    """Função principal para configurar o ambiente de teste"""
    print_header("CONFIGURADOR DE AMBIENTE DE TESTE")
    print("Sistema: SISVENDA - Testes das User Stories 7, 8 e 9")
    
    # Verificar versão do Python
    verificar_python()
    
    # Criar ambiente virtual
    if not criar_ambiente_virtual():
        print("❌ Falha na configuração do ambiente virtual.")
        return False
    
    # Instalar dependências
    venv_path = "venv_teste"
    if not instalar_dependencias(venv_path):
        print("❌ Falha na instalação das dependências.")
        return False
    
    print_header("CONFIGURAÇÃO CONCLUÍDA COM SUCESSO!")
    
    # Instruções finais
    if platform.system() == "Windows":
        print("📝 Para ativar o ambiente virtual, execute:")
        print("   venv_teste\\Scripts\\activate")
    else:
        print("📝 Para ativar o ambiente virtual, execute:")
        print("   source venv_teste/bin/activate")
    
    print("\n📝 Para executar os testes, ative o ambiente virtual e execute:")
    print("   python executar_testes.py")
    
    print("\n📝 Para gerar os gráficos do relatório, execute:")
    print("   python gerar_graficos_relatorio.py")
    
    print("\n📝 Para verificar a cobertura de código, execute:")
    print("   coverage run --source='.' manage.py test produto.tests.GerenteEstoqueTestCase")
    print("   coverage report")
    print("   coverage html  # para um relatório detalhado em HTML")
    
    return True

if __name__ == "__main__":
    configurar_ambiente()

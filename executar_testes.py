#!/usr/bin/env python
"""
Script para executar os testes automatizados das User Stories 7, 8 e 9
Sistema de Vendas - Funcionalidades do Gerente de Estoque

Como usar:
1. Execute no terminal: python executar_testes.py
2. Ou execute via Django: python manage.py test produto.tests.GerenteEstoqueTestCase -v 2

User Stories testadas:
- US7: Gerente de estoque – Programar entrega
- US8: Gerente de estoque – Processar entrega  
- US9: Gerente de estoque – Relatórios de produtos
"""

import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

def setup_django():
    """Configurar Django para execução dos testes"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sisvenda.settings')
    django.setup()

def executar_testes():
    """Executar suite completa de testes"""
    print("🚀 Iniciando execução dos testes automatizados...")
    print("📋 User Stories: 7, 8 e 9 - Gerente de Estoque")
    print("="*60)
    
    # Configurar Django
    setup_django()
    
    # Importar a classe de teste
    from produto.tests import GerenteEstoqueTestCase
    
    # Criar instância e executar suite completa
    suite_testes = GerenteEstoqueTestCase()
    suite_testes.setUp()
    suite_testes.executar_suite_completa()

def executar_teste_especifico(nome_teste):
    """Executar um teste específico"""
    setup_django()
    from produto.tests import GerenteEstoqueTestCase
    
    suite_testes = GerenteEstoqueTestCase()
    suite_testes.setUp()
    
    if hasattr(suite_testes, nome_teste):
        print(f"🎯 Executando teste específico: {nome_teste}")
        getattr(suite_testes, nome_teste)()
    else:
        print(f"❌ Teste '{nome_teste}' não encontrado")

def listar_testes_disponiveis():
    """Listar todos os testes disponíveis"""
    setup_django()
    from produto.tests import GerenteEstoqueTestCase
    
    print("📋 Testes disponíveis:")
    print("="*50)
    
    suite_testes = GerenteEstoqueTestCase()
    metodos = [m for m in dir(suite_testes) if m.startswith('test_')]
    
    for i, metodo in enumerate(metodos, 1):
        docstring = getattr(suite_testes, metodo).__doc__ or "Sem descrição"
        print(f"{i:2d}. {metodo}")
        print(f"    {docstring.strip()}")
        print()

def menu_interativo():
    """Menu interativo para execução dos testes"""
    while True:
        print("\n" + "="*60)
        print("🧪 SISTEMA DE TESTES AUTOMATIZADOS")
        print("📋 User Stories 7, 8 e 9 - Gerente de Estoque")
        print("="*60)
        print("1. Executar TODOS os testes (Suite Completa)")
        print("2. Listar testes disponíveis")
        print("3. Executar teste específico")
        print("4. Executar testes via Django (recomendado)")
        print("5. Sair")
        print("="*60)
        
        opcao = input("👉 Escolha uma opção: ").strip()
        
        if opcao == '1':
            executar_testes()
            
        elif opcao == '2':
            listar_testes_disponiveis()
            
        elif opcao == '3':
            nome_teste = input("Digite o nome do teste (ex: test_us7_listar_pedidos_aprovados): ").strip()
            if nome_teste:
                executar_teste_especifico(nome_teste)
            else:
                print("❌ Nome do teste não pode estar vazio")
                
        elif opcao == '4':
            print("\n📝 Execute no terminal:")
            print("python manage.py test produto.tests.GerenteEstoqueTestCase -v 2")
            print("\n📝 Para um teste específico:")
            print("python manage.py test produto.tests.GerenteEstoqueTestCase.test_us7_listar_pedidos_aprovados -v 2")
            
        elif opcao == '5':
            print("👋 Saindo... Obrigado por usar o sistema de testes!")
            break
            
        else:
            print("❌ Opção inválida. Tente novamente.")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        comando = sys.argv[1]
        
        if comando == 'listar':
            listar_testes_disponiveis()
        elif comando == 'todos':
            executar_testes()
        elif comando.startswith('test_'):
            executar_teste_especifico(comando)
        else:
            print("❌ Comando inválido")
            print("📝 Comandos disponíveis:")
            print("  python executar_testes.py todos")
            print("  python executar_testes.py listar")
            print("  python executar_testes.py test_us7_listar_pedidos_aprovados")
    else:
        menu_interativo()

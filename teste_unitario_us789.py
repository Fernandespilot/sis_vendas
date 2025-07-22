#!/usr/bin/env python
"""
TESTE UNITÁRIO AUTOMATIZADO
User Stories 7, 8 e 9 - Gerente de Estoque
Sistema de Vendas - Django
"""
import os
import sys
import django
from decimal import Decimal
from datetime import date, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sisvenda.settings')
django.setup()

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.utils import timezone
from produto.models import Produto


class TesteSimplesUS789(TestCase):
    """Teste unitário simplificado para US7, US8 e US9"""
    
    def setUp(self):
        """Configuração inicial"""
        self.client = Client()
        
        # Criar usuário gerente
        self.gerente = User.objects.create_user(
            username='gerente_teste',
            password='senha123',
            email='gerente@teste.com'
        )
        
        # Criar produtos para teste
        self.produto_alto = Produto.objects.create(
            nome='Notebook Dell Inspiron',
            descricao='Notebook para escritório',
            preco=Decimal('2500.00'),
            estoque=25
        )
        
        self.produto_baixo = Produto.objects.create(
            nome='Mouse Logitech MX',
            descricao='Mouse ergonômico',
            preco=Decimal('45.00'),
            estoque=3
        )
        
        self.produto_promocao = Produto.objects.create(
            nome='Cabo USB Barato',
            descricao='Cabo USB 2.0',
            preco=Decimal('15.00'),
            estoque=50
        )
        
        # Login do gerente
        login_success = self.client.login(username='gerente_teste', password='senha123')
        if not login_success:
            raise Exception("Falha no login do gerente")

    def test_us7_acesso_pedidos_aprovados(self):
        """US7: Testar acesso à página de pedidos aprovados"""
        print("\n🧪 TESTE US7 - Acesso Pedidos Aprovados")
        
        response = self.client.get('/venda/pedidos-aprovados/')
        
        assert response.status_code == 200, f"Esperado 200, obtido {response.status_code}"
        assert 'vendas' in response.context, "Context 'vendas' não encontrado"
        
        print("✅ US7 - Página de pedidos aprovados acessível")
        return True

    def test_us8_acesso_entregas_hoje(self):
        """US8: Testar acesso à página de entregas de hoje"""
        print("\n🧪 TESTE US8 - Acesso Entregas Hoje")
        
        response = self.client.get('/venda/entregas-hoje/')
        
        assert response.status_code == 200, f"Esperado 200, obtido {response.status_code}"
        assert 'entregas' in response.context, "Context 'entregas' não encontrado"
        assert 'data_hoje' in response.context, "Context 'data_hoje' não encontrado"
        
        print("✅ US8 - Página de entregas de hoje acessível")
        return True

    def test_us9_relatorio_estoque_baixo(self):
        """US9: Testar relatório de estoque baixo"""
        print("\n🧪 TESTE US9 - Relatório Estoque Baixo")
        
        response = self.client.get('/venda/relatorio/estoque-baixo/')
        
        assert response.status_code == 200, f"Esperado 200, obtido {response.status_code}"
        assert 'produtos' in response.context, "Context 'produtos' não encontrado"
        assert 'limite' in response.context, "Context 'limite' não encontrado"
        
        # Verificar lógica do relatório
        produtos = response.context['produtos']
        limite = response.context['limite']
        
        for produto in produtos:
            assert produto.estoque <= limite, f"Produto {produto.nome} tem estoque {produto.estoque} > {limite}"
        
        print(f"✅ US9 - Relatório estoque baixo funcionando (limite: {limite})")
        return True

    def test_us9_relatorio_promocao(self):
        """US9: Testar relatório de promoção"""
        print("\n🧪 TESTE US9 - Relatório Promoção")
        
        response = self.client.get('/venda/relatorio/promocao/')
        
        assert response.status_code == 200, f"Esperado 200, obtido {response.status_code}"
        assert 'produtos' in response.context, "Context 'produtos' não encontrado"
        
        # Verificar lógica do relatório (preço < 50)
        produtos = response.context['produtos']
        
        for produto in produtos:
            assert produto.preco < 50, f"Produto {produto.nome} tem preço R$ {produto.preco} >= R$ 50"
        
        print("✅ US9 - Relatório promoção funcionando")
        return True

    def test_us9_relatorio_por_grupo(self):
        """US9: Testar relatório por grupo de preço"""
        print("\n🧪 TESTE US9 - Relatório Por Grupo")
        
        response = self.client.get('/venda/relatorio/por-grupo/')
        
        assert response.status_code == 200, f"Esperado 200, obtido {response.status_code}"
        assert 'produtos_baixo' in response.context, "Context 'produtos_baixo' não encontrado"
        assert 'produtos_medio' in response.context, "Context 'produtos_medio' não encontrado"
        assert 'produtos_alto' in response.context, "Context 'produtos_alto' não encontrado"
        
        # Verificar agrupamento
        baixo = response.context['produtos_baixo']
        medio = response.context['produtos_medio']
        alto = response.context['produtos_alto']
        
        for produto in baixo:
            assert produto.preco < 50, f"Produto {produto.nome} no grupo errado"
        
        for produto in medio:
            assert 50 <= produto.preco < 100, f"Produto {produto.nome} no grupo errado"
        
        for produto in alto:
            assert produto.preco >= 100, f"Produto {produto.nome} no grupo errado"
        
        print("✅ US9 - Relatório por grupo funcionando")
        return True

    def test_us9_exportacao_pdf(self):
        """US9: Testar exportação PDF"""
        print("\n🧪 TESTE US9 - Exportação PDF")
        
        tipos = ['estoque_baixo', 'promocao', 'geral']
        
        for tipo in tipos:
            response = self.client.get(f'/venda/relatorio/pdf/{tipo}/')
            
            assert response.status_code == 200, f"PDF {tipo}: Esperado 200, obtido {response.status_code}"
            assert response['Content-Type'] == 'application/pdf', f"PDF {tipo}: Content-Type incorreto"
            assert 'attachment' in response['Content-Disposition'], f"PDF {tipo}: Disposition incorreto"
        
        print("✅ US9 - Exportação PDF funcionando")
        return True

    def test_us9_exportacao_excel(self):
        """US9: Testar exportação Excel"""
        print("\n🧪 TESTE US9 - Exportação Excel")
        
        tipos = ['estoque_baixo', 'promocao', 'geral']
        expected_content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        
        for tipo in tipos:
            response = self.client.get(f'/venda/relatorio/excel/{tipo}/')
            
            assert response.status_code == 200, f"Excel {tipo}: Esperado 200, obtido {response.status_code}"
            assert response['Content-Type'] == expected_content_type, f"Excel {tipo}: Content-Type incorreto"
            assert 'attachment' in response['Content-Disposition'], f"Excel {tipo}: Disposition incorreto"
        
        print("✅ US9 - Exportação Excel funcionando")
        return True

    def test_controle_acesso(self):
        """Testar controle de acesso sem login"""
        print("\n🧪 TESTE - Controle de Acesso")
        
        # Fazer logout
        self.client.logout()
        
        urls_protegidas = [
            '/venda/pedidos-aprovados/',
            '/venda/entregas-hoje/',
            '/venda/relatorios/',
            '/venda/relatorio/estoque-baixo/',
            '/venda/relatorio/promocao/'
        ]
        
        for url in urls_protegidas:
            response = self.client.get(url)
            assert response.status_code in [302, 403], f"URL {url} não está protegida: {response.status_code}"
        
        print("✅ Controle de acesso funcionando")
        return True

    def executar_todos_os_testes(self):
        """Executar todos os testes e gerar relatório"""
        print("\n" + "="*80)
        print("🚀 EXECUTANDO TESTE UNITÁRIO AUTOMATIZADO")
        print("📋 User Stories: 7, 8 e 9 - Gerente de Estoque")
        print("🎯 Sistema de Vendas - Django Application")
        print("="*80)
        
        testes = [
            ("US7 - Acesso Pedidos Aprovados", self.test_us7_acesso_pedidos_aprovados),
            ("US8 - Acesso Entregas Hoje", self.test_us8_acesso_entregas_hoje),
            ("US9 - Relatório Estoque Baixo", self.test_us9_relatorio_estoque_baixo),
            ("US9 - Relatório Promoção", self.test_us9_relatorio_promocao),
            ("US9 - Relatório Por Grupo", self.test_us9_relatorio_por_grupo),
            ("US9 - Exportação PDF", self.test_us9_exportacao_pdf),
            ("US9 - Exportação Excel", self.test_us9_exportacao_excel),
            ("Controle de Acesso", self.test_controle_acesso)
        ]
        
        resultados = []
        total = len(testes)
        sucesso = 0
        
        for nome, funcao in testes:
            try:
                funcao()
                resultados.append((nome, "✅ PASSOU"))
                sucesso += 1
            except Exception as e:
                resultados.append((nome, f"❌ FALHOU: {str(e)}"))
        
        # Relatório Final
        print("\n" + "="*80)
        print("📊 RELATÓRIO FINAL DO TESTE UNITÁRIO")
        print("="*80)
        
        for nome, status in resultados:
            print(f"{status} | {nome}")
        
        print("\n" + "-"*80)
        print(f"📈 Total de testes: {total}")
        print(f"✅ Testes aprovados: {sucesso}")
        print(f"❌ Testes falharam: {total - sucesso}")
        print(f"📊 Taxa de sucesso: {(sucesso/total)*100:.1f}%")
        
        if sucesso == total:
            print("\n🎉 TODOS OS TESTES PASSARAM!")
            print("✅ User Stories 7, 8 e 9 estão funcionando corretamente")
            print("🚀 Sistema pronto para validação final")
        else:
            print(f"\n⚠️  {total - sucesso} teste(s) falharam")
            print("🔧 Revise as implementações que falharam")
        
        print("="*80)
        
        return sucesso == total


def main():
    """Função principal para executar os testes"""
    try:
        # Configurar teste
        teste = TesteSimplesUS789()
        teste.setUp()
        
        # Executar todos os testes
        resultado = teste.executar_todos_os_testes()
        
        return 0 if resultado else 1
        
    except Exception as e:
        print(f"❌ ERRO CRÍTICO: {str(e)}")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)

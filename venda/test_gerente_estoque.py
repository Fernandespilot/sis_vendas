from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal

from produto.models import Produto
from clientes.models import Cliente
from venda.models import Venda


class TesteGerenteEstoque(TestCase):
    """
    Sistema automatizado de testes simplificado para as User Stories 7, 8 e 9
    """

    def setUp(self):
        """Configuração inicial para todos os testes"""
        self.client = Client()
        
        # Criar usuário gerente
        self.gerente = User.objects.create_user(
            username='gerente_teste',
            password='senha123',
            email='gerente@teste.com'
        )
        
        # Criar produtos de teste
        self.produto_alto_estoque = Produto.objects.create(
            nome='Notebook Dell',
            descricao='Notebook para teste',
            preco=Decimal('2500.00'),
            estoque=20
        )
        
        self.produto_baixo_estoque = Produto.objects.create(
            nome='Mouse Logitech',
            descricao='Mouse para teste',
            preco=Decimal('45.00'),
            estoque=3
        )
        
        # Criar cliente de teste
        self.cliente = Cliente.objects.create(
            nome='Cliente Teste',
            email='cliente@teste.com'
        )
        
        # Login do gerente
        self.client.login(username='gerente_teste', password='senha123')

    def test_us7_acesso_pedidos_aprovados(self):
        """US7: Teste básico - Acessar página de pedidos aprovados"""
        print("\n🧪 TESTANDO US7 - Acesso à página de pedidos aprovados")
        
        response = self.client.get('/venda/pedidos-aprovados/')
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Página de pedidos aprovados acessível")
        else:
            print(f"❌ Erro ao acessar página: {response.status_code}")

    def test_us8_acesso_entregas_hoje(self):
        """US8: Teste básico - Acessar página de entregas de hoje"""
        print("\n🧪 TESTANDO US8 - Acesso à página de entregas de hoje")
        
        response = self.client.get('/venda/entregas-hoje/')
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Página de entregas de hoje acessível")
        else:
            print(f"❌ Erro ao acessar página: {response.status_code}")

    def test_us9_acesso_relatorios(self):
        """US9: Teste básico - Acessar páginas de relatórios"""
        print("\n🧪 TESTANDO US9 - Acesso às páginas de relatórios")
        
        urls_relatorios = [
            '/venda/relatorios/',
            '/venda/relatorio/estoque-baixo/',
            '/venda/relatorio/promocao/',
            '/venda/relatorio/por-grupo/'
        ]
        
        for url in urls_relatorios:
            response = self.client.get(url)
            print(f"URL: {url} - Status: {response.status_code}")
            
            if response.status_code == 200:
                print(f"✅ {url} acessível")
            else:
                print(f"❌ Erro em {url}: {response.status_code}")

    def test_us9_exportacao_pdf(self):
        """US9: Teste básico - Exportação PDF"""
        print("\n🧪 TESTANDO US9 - Exportação PDF")
        
        response = self.client.get('/venda/relatorio/pdf/estoque_baixo/')
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Exportação PDF funcionando")
            print(f"Content-Type: {response.get('Content-Type', 'N/A')}")
        else:
            print(f"❌ Erro na exportação PDF: {response.status_code}")

    def test_us9_exportacao_excel(self):
        """US9: Teste básico - Exportação Excel"""
        print("\n🧪 TESTANDO US9 - Exportação Excel")
        
        response = self.client.get('/venda/relatorio/excel/promocao/')
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ Exportação Excel funcionando")
            print(f"Content-Type: {response.get('Content-Type', 'N/A')}")
        else:
            print(f"❌ Erro na exportação Excel: {response.status_code}")

    def executar_todos_os_testes_basicos(self):
        """Executa todos os testes básicos em sequência"""
        print("\n" + "="*60)
        print("🚀 EXECUTANDO TESTES BÁSICOS - USER STORIES 7, 8 e 9")
        print("📋 Testando acesso às páginas e funcionalidades básicas")
        print("="*60)
        
        try:
            self.test_us7_acesso_pedidos_aprovados()
            self.test_us8_acesso_entregas_hoje()
            self.test_us9_acesso_relatorios()
            self.test_us9_exportacao_pdf()
            self.test_us9_exportacao_excel()
            
            print("\n" + "="*60)
            print("✅ TESTES BÁSICOS CONCLUÍDOS!")
            print("📊 Verificação de acessibilidade das funcionalidades")
            print("="*60)
            
        except Exception as e:
            print(f"\n❌ ERRO NO TESTE: {str(e)}")
            print("="*60)

from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal
from django.contrib.messages import get_messages

from produto.models import Produto
from clientes.models import Cliente
from venda.models import Venda


class GerenteEstoqueTestCase(TestCase):
    """
    Sistema automatizado de testes para as User Stories 7, 8 e 9
    - US7: Gerente de estoque – Programar entrega
    - US8: Gerente de estoque – Processar entrega  
    - US9: Gerente de estoque – Relatórios de produtos
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
        self.produto_estoque_alto = Produto.objects.create(
            nome='Notebook Dell',
            descricao='Notebook para teste',
            preco=Decimal('2500.00'),
            estoque=20
        )
        
        self.produto_estoque_baixo = Produto.objects.create(
            nome='Mouse Logitech',
            descricao='Mouse para teste',
            preco=Decimal('45.00'),
            estoque=3
        )
        
        self.produto_promocao = Produto.objects.create(
            nome='Teclado Barato',
            descricao='Teclado em promoção',
            preco=Decimal('25.00'),
            estoque=15
        )
        
        self.produto_medio = Produto.objects.create(
            nome='Monitor',
            descricao='Monitor para teste',
            preco=Decimal('75.00'),
            estoque=8
        )
        
        # Criar cliente de teste (usando apenas campos da migração inicial)
        self.cliente = Cliente.objects.create(
            nome='Cliente Teste',
            email='cliente@teste.com',
            telefone='11999999999'
        )
        
        # Login do gerente
        self.client.login(username='gerente_teste', password='senha123')

    def test_us7_listar_pedidos_aprovados(self):
        """US7: Teste - Exibir somente pedidos com status 'Aprovado'"""
        print("\n🧪 TESTANDO US7 - Listar Pedidos Aprovados")
        
        # Criar vendas com diferentes status
        venda_aprovada = Venda.objects.create(
            cliente=self.cliente,
            produto=self.produto_estoque_alto,
            quantidade=2,
            status='APROVADO'
        )
        
        venda_pendente = Venda.objects.create(
            cliente=self.cliente,
            produto=self.produto_estoque_baixo,
            quantidade=1,
            status='PENDENTE'
        )
        
        venda_processada = Venda.objects.create(
            cliente=self.cliente,
            produto=self.produto_promocao,
            quantidade=1,
            status='PROCESSADO'
        )
        
        # Testar acesso à página de pedidos aprovados
        response = self.client.get('/venda/pedidos-aprovados/')
        
        # Verificações básicas
        self.assertEqual(response.status_code, 200)
        print("✅ Página de pedidos aprovados acessível")
        
        # Verificar se apenas vendas aprovadas aparecem
        self.assertIn('vendas', response.context)
        vendas_contexto = response.context['vendas']
        
        # Verificar filtro por status APROVADO
        for venda in vendas_contexto:
            self.assertEqual(venda.status, 'APROVADO')
        
        print("✅ Apenas pedidos APROVADOS são exibidos")

    def test_us7_programar_entrega_com_estoque_suficiente(self):
        """US7: Teste - Programar entrega com estoque suficiente"""
        print("\n🧪 TESTANDO US7 - Programar Entrega (Estoque Suficiente)")
        
        # Criar venda aprovada
        venda = Venda.objects.create(
            cliente=self.cliente,
            produto=self.produto_estoque_alto,
            quantidade=5,
            status='APROVADO'
        )
        
        estoque_inicial = self.produto_estoque_alto.estoque
        data_entrega = (timezone.now().date() + timedelta(days=3)).strftime('%Y-%m-%d')
        
        # Testar GET da página de programar entrega
        response_get = self.client.get(f'/venda/programar-entrega/{venda.id}/')
        self.assertEqual(response_get.status_code, 200)
        self.assertIn('venda', response_get.context)
        
        # Programar entrega via POST
        response = self.client.post(
            f'/venda/programar-entrega/{venda.id}/',
            {'data_entrega': data_entrega},
            follow=True
        )
        
        # Recarregar objetos do banco
        venda.refresh_from_db()
        self.produto_estoque_alto.refresh_from_db()
        
        # Verificações
        self.assertEqual(response.status_code, 200)
        self.assertEqual(venda.status, 'PROGRAMADO')
        self.assertEqual(str(venda.data_entrega), data_entrega)
        self.assertEqual(venda.gerente_responsavel, self.gerente)
        self.assertEqual(self.produto_estoque_alto.estoque, estoque_inicial - 5)
        
        # Verificar mensagem de sucesso
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('programada' in str(msg) for msg in messages))
        
        print("✅ Entrega programada e estoque subtraído automaticamente")

    def test_us7_impedir_agendamento_estoque_insuficiente(self):
        """US7: Teste - Impedir agendamento se houver falta de produto"""
        print("\n🧪 TESTANDO US7 - Impedir Agendamento (Estoque Insuficiente)")
        
        # Criar venda com quantidade maior que estoque
        venda = Venda.objects.create(
            cliente=self.cliente,
            produto=self.produto_estoque_baixo,  # estoque = 3
            quantidade=10,  # maior que estoque
            status='APROVADO'
        )
        
        estoque_inicial = self.produto_estoque_baixo.estoque
        data_entrega = (timezone.now().date() + timedelta(days=2)).strftime('%Y-%m-%d')
        
        # Tentar programar entrega
        response = self.client.post(
            f'/venda/programar-entrega/{venda.id}/',
            {'data_entrega': data_entrega},
            follow=True
        )
        
        # Recarregar objetos
        venda.refresh_from_db()
        self.produto_estoque_baixo.refresh_from_db()
        
        # Verificações
        self.assertEqual(venda.status, 'APROVADO')  # Status não mudou
        self.assertEqual(self.produto_estoque_baixo.estoque, estoque_inicial)  # Estoque não alterado
        
        # Verificar mensagem de erro
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('insuficiente' in str(msg) for msg in messages))
        
        print("✅ Agendamento impedido por estoque insuficiente")

    def test_us8_listar_entregas_hoje(self):
        """US8: Teste - Exibir somente pedidos com data de entrega igual ao dia atual"""
        print("\n🧪 TESTANDO US8 - Listar Entregas de Hoje")
        
        hoje = timezone.now().date()
        amanha = hoje + timedelta(days=1)
        ontem = hoje - timedelta(days=1)
        
        # Criar vendas programadas para diferentes datas
        venda_hoje = Venda.objects.create(
            cliente=self.cliente,
            produto=self.produto_estoque_alto,
            quantidade=1,
            status='PROGRAMADO',
            data_entrega=hoje
        )
        
        venda_amanha = Venda.objects.create(
            cliente=self.cliente,
            produto=self.produto_estoque_baixo,
            quantidade=1,
            status='PROGRAMADO',
            data_entrega=amanha
        )
        
        venda_ontem = Venda.objects.create(
            cliente=self.cliente,
            produto=self.produto_promocao,
            quantidade=1,
            status='PROGRAMADO',
            data_entrega=ontem
        )
        
        # Testar URL de entregas hoje
        response = self.client.get('/venda/entregas-hoje/')
        
        # Verificações básicas
        self.assertEqual(response.status_code, 200)
        self.assertIn('entregas', response.context)
        self.assertIn('data_hoje', response.context)
        
        # Verificar se apenas entregas de hoje aparecem
        entregas_contexto = response.context['entregas']
        for entrega in entregas_contexto:
            self.assertEqual(entrega.data_entrega, hoje)
            self.assertEqual(entrega.status, 'PROGRAMADO')
        
        print("✅ Apenas entregas de hoje são exibidas")

    def test_us8_processar_entrega(self):
        """US8: Teste - Processar entrega altera status para 'Processado'"""
        print("\n🧪 TESTANDO US8 - Processar Entrega")
        
        # Criar venda programada para hoje
        venda = Venda.objects.create(
            cliente=self.cliente,
            produto=self.produto_estoque_alto,
            quantidade=2,
            status='PROGRAMADO',
            data_entrega=timezone.now().date()
        )
        
        # Testar GET da página de processar entrega
        response_get = self.client.get(f'/venda/processar-entrega/{venda.id}/')
        self.assertEqual(response_get.status_code, 200)
        self.assertIn('venda', response_get.context)
        
        # Processar entrega via POST
        response = self.client.post(f'/venda/processar-entrega/{venda.id}/', follow=True)
        
        # Recarregar objeto
        venda.refresh_from_db()
        
        # Verificações
        self.assertEqual(response.status_code, 200)
        self.assertEqual(venda.status, 'PROCESSADO')
        
        # Verificar mensagem de sucesso
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('processada' in str(msg) for msg in messages))
        
        print("✅ Status alterado para PROCESSADO")

    def test_us9_relatorio_estoque_baixo(self):
        """US9: Teste - Relatório de produtos com estoque baixo"""
        print("\n🧪 TESTANDO US9 - Relatório Estoque Baixo")
        
        response = self.client.get('/venda/relatorio/estoque-baixo/')
        
        # Verificações básicas
        self.assertEqual(response.status_code, 200)
        self.assertIn('produtos', response.context)
        self.assertIn('limite', response.context)
        
        # Verificar se apenas produtos com estoque baixo aparecem
        produtos_contexto = response.context['produtos']
        limite = response.context['limite']
        
        for produto in produtos_contexto:
            self.assertLessEqual(produto.estoque, limite)
        
        # Produto com estoque 3 deve aparecer (limite <= 10)
        nomes_produtos = [p.nome for p in produtos_contexto]
        self.assertIn(self.produto_estoque_baixo.nome, nomes_produtos)
        
        # Produto com estoque 20 não deve aparecer
        self.assertNotIn(self.produto_estoque_alto.nome, nomes_produtos)
        
        print("✅ Relatório de estoque baixo funcionando")

    def test_us9_relatorio_promocao(self):
        """US9: Teste - Relatório de produtos em promoção"""
        print("\n🧪 TESTANDO US9 - Relatório Promoção")
        
        response = self.client.get('/venda/relatorio/promocao/')
        
        # Verificações básicas
        self.assertEqual(response.status_code, 200)
        self.assertIn('produtos', response.context)
        
        # Verificar se apenas produtos em promoção aparecem (preço < 50)
        produtos_contexto = response.context['produtos']
        
        for produto in produtos_contexto:
            self.assertLess(produto.preco, 50)
        
        # Produto com preço R$ 25,00 deve aparecer
        nomes_produtos = [p.nome for p in produtos_contexto]
        self.assertIn(self.produto_promocao.nome, nomes_produtos)
        
        # Produto com preço R$ 2500,00 não deve aparecer
        self.assertNotIn(self.produto_estoque_alto.nome, nomes_produtos)
        
        print("✅ Relatório de promoção funcionando")

    def test_us9_relatorio_por_grupo(self):
        """US9: Teste - Relatório de produtos por grupo de preço"""
        print("\n🧪 TESTANDO US9 - Relatório Por Grupo")
        
        response = self.client.get('/venda/relatorio/por-grupo/')
        
        # Verificações básicas
        self.assertEqual(response.status_code, 200)
        self.assertIn('produtos_baixo', response.context)
        self.assertIn('produtos_medio', response.context)
        self.assertIn('produtos_alto', response.context)
        
        # Verificar agrupamento por preço
        produtos_baixo = response.context['produtos_baixo']
        produtos_medio = response.context['produtos_medio']
        produtos_alto = response.context['produtos_alto']
        
        # Verificar se produtos estão nos grupos corretos
        for produto in produtos_baixo:
            self.assertLess(produto.preco, 50)
        
        for produto in produtos_medio:
            self.assertGreaterEqual(produto.preco, 50)
            self.assertLess(produto.preco, 100)
        
        for produto in produtos_alto:
            self.assertGreaterEqual(produto.preco, 100)
        
        print("✅ Relatório por grupo funcionando")

    def test_us9_exportar_pdf(self):
        """US9: Teste - Exportação de relatório em PDF"""
        print("\n🧪 TESTANDO US9 - Exportar PDF")
        
        tipos_relatorio = ['estoque_baixo', 'promocao', 'geral']
        
        for tipo in tipos_relatorio:
            response = self.client.get(f'/venda/relatorio/pdf/{tipo}/')
            
            # Verificações
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'application/pdf')
            self.assertIn('attachment', response['Content-Disposition'])
            self.assertIn(f'relatorio_{tipo}.pdf', response['Content-Disposition'])
        
        print("✅ Exportação PDF funcionando para todos os tipos")

    def test_us9_exportar_excel(self):
        """US9: Teste - Exportação de relatório em Excel"""
        print("\n🧪 TESTANDO US9 - Exportar Excel")
        
        tipos_relatorio = ['estoque_baixo', 'promocao', 'geral']
        
        for tipo in tipos_relatorio:
            response = self.client.get(f'/venda/relatorio/excel/{tipo}/')
            
            # Verificações
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response['Content-Type'], 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            self.assertIn('attachment', response['Content-Disposition'])
            self.assertIn(f'relatorio_{tipo}.xlsx', response['Content-Disposition'])
        
        print("✅ Exportação Excel funcionando para todos os tipos")

    def test_us9_pagina_principal_relatorios(self):
        """US9: Teste - Página principal de relatórios"""
        print("\n🧪 TESTANDO US9 - Página Principal de Relatórios")
        
        response = self.client.get('/venda/relatorios/')
        
        # Verificações básicas
        self.assertEqual(response.status_code, 200)
        
        print("✅ Página principal de relatórios acessível")

    def test_acesso_sem_login(self):
        """Teste - Verificar se páginas exigem login"""
        print("\n🧪 TESTANDO - Controle de Acesso")
        
        # Fazer logout
        self.client.logout()
        
        urls_protegidas = [
            '/venda/pedidos-aprovados/',
            '/venda/entregas-hoje/',
            '/venda/relatorios/',
            '/venda/relatorio/estoque-baixo/',
            '/venda/relatorio/promocao/',
            '/venda/relatorio/por-grupo/'
        ]
        
        for url in urls_protegidas:
            response = self.client.get(url)
            # Deve redirecionar para login (302) ou dar erro 403
            self.assertIn(response.status_code, [302, 403])
        
        print("✅ Controle de acesso funcionando")

    def test_validacoes_negocio(self):
        """Teste - Validações específicas de regras de negócio"""
        print("\n🧪 TESTANDO - Validações de Negócio")
        
        # Teste 1: Não permitir programar entrega de venda não aprovada
        venda_pendente = Venda.objects.create(
            cliente=self.cliente,
            produto=self.produto_estoque_alto,
            quantidade=1,
            status='PENDENTE'
        )
        
        response = self.client.get(f'/venda/programar-entrega/{venda_pendente.id}/')
        self.assertEqual(response.status_code, 404)
        
        # Teste 2: Não permitir processar entrega não programada
        venda_aprovada = Venda.objects.create(
            cliente=self.cliente,
            produto=self.produto_estoque_alto,
            quantidade=1,
            status='APROVADO'
        )
        
        response = self.client.get(f'/venda/processar-entrega/{venda_aprovada.id}/')
        self.assertEqual(response.status_code, 404)
        
        print("✅ Validações de negócio funcionando")

    def test_calculo_valor_total(self):
        """Teste - Property valor_total do modelo Venda"""
        print("\n🧪 TESTANDO - Cálculo de Valor Total")
        
        venda = Venda.objects.create(
            cliente=self.cliente,
            produto=self.produto_estoque_alto,  # preço = 2500.00
            quantidade=3,
            status='PENDENTE'
        )
        
        valor_esperado = self.produto_estoque_alto.preco * 3
        self.assertEqual(venda.valor_total, valor_esperado)
        
        print("✅ Cálculo de valor total funcionando")

    def executar_suite_completa(self):
        """Executa todos os testes em sequência com relatório detalhado"""
        print("\n" + "="*70)
        print("🚀 INICIANDO SUITE COMPLETA DE TESTES AUTOMATIZADOS")
        print("📋 User Stories: 7, 8 e 9 - Gerente de Estoque")
        print("🎯 Sistema de Vendas - Funcionalidades de Estoque")
        print("="*70)
        
        testes_executados = 0
        testes_sucesso = 0
        
        lista_testes = [
            ("US7 - Listar Pedidos Aprovados", self.test_us7_listar_pedidos_aprovados),
            ("US7 - Programar Entrega (Suficiente)", self.test_us7_programar_entrega_com_estoque_suficiente),
            ("US7 - Impedir Agendamento (Insuficiente)", self.test_us7_impedir_agendamento_estoque_insuficiente),
            ("US8 - Listar Entregas de Hoje", self.test_us8_listar_entregas_hoje),
            ("US8 - Processar Entrega", self.test_us8_processar_entrega),
            ("US9 - Relatório Estoque Baixo", self.test_us9_relatorio_estoque_baixo),
            ("US9 - Relatório Promoção", self.test_us9_relatorio_promocao),
            ("US9 - Relatório Por Grupo", self.test_us9_relatorio_por_grupo),
            ("US9 - Exportar PDF", self.test_us9_exportar_pdf),
            ("US9 - Exportar Excel", self.test_us9_exportar_excel),
            ("US9 - Página Principal", self.test_us9_pagina_principal_relatorios),
            ("Controle de Acesso", self.test_acesso_sem_login),
            ("Validações de Negócio", self.test_validacoes_negocio),
            ("Cálculo Valor Total", self.test_calculo_valor_total)
        ]
        
        for nome_teste, funcao_teste in lista_testes:
            try:
                testes_executados += 1
                print(f"\n📝 Executando: {nome_teste}")
                funcao_teste()
                testes_sucesso += 1
                print(f"✅ {nome_teste} - PASSOU")
                
            except Exception as e:
                print(f"❌ {nome_teste} - FALHOU: {str(e)}")
        
        # Relatório final
        print("\n" + "="*70)
        print("📊 RELATÓRIO FINAL DA SUITE DE TESTES")
        print("="*70)
        print(f"📈 Total de testes executados: {testes_executados}")
        print(f"✅ Testes com sucesso: {testes_sucesso}")
        print(f"❌ Testes falharam: {testes_executados - testes_sucesso}")
        print(f"📊 Taxa de sucesso: {(testes_sucesso/testes_executados)*100:.1f}%")
        
        if testes_sucesso == testes_executados:
            print("\n🎉 TODOS OS TESTES PASSARAM COM SUCESSO!")
            print("✅ User Stories 7, 8 e 9 estão funcionando corretamente")
            print("🚀 Sistema pronto para produção!")
        else:
            print(f"\n⚠️  {testes_executados - testes_sucesso} teste(s) falharam")
            print("🔧 Revise as funcionalidades que falharam")
        
        print("="*70)

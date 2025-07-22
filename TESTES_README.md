# Sistema Automatizado de Testes - User Stories 7, 8 e 9

## 📋 Funcionalidades Testadas

### **User Story 7: Gerente de estoque – Programar entrega**
- ✅ Exibir somente pedidos com status "Aprovado"
- ✅ Escolher data de entrega e subtrair estoque automaticamente
- ✅ Impedir agendamento se houver falta de produto
- ✅ Status atualizado para "Programado" com atribuição do gerente responsável

### **User Story 8: Gerente de estoque – Processar entrega**
- ✅ Exibir somente pedidos com data de entrega igual ao dia atual
- ✅ Botão "Processar entrega" altera status para "Processado"
- ✅ Validações de negócio para estado dos pedidos

### **User Story 9: Gerente de estoque – Relatórios de produtos**
- ✅ Relatório de produtos com estoque baixo (≤ 10 unidades)
- ✅ Relatório de produtos em promoção (preço < R$ 50,00)
- ✅ Relatório de produtos por grupo de preço
- ✅ Exportação em PDF e Excel com confirmação

## 🧪 Como Executar os Testes

### **Método 1: Django Test Framework (Recomendado)**
```bash
# Executar todos os testes
python manage.py test produto.tests.GerenteEstoqueTestCase -v 2

# Executar teste específico
python manage.py test produto.tests.GerenteEstoqueTestCase.test_us7_listar_pedidos_aprovados -v 2

# Executar com coverage (se instalado)
coverage run --source='.' manage.py test produto.tests.GerenteEstoqueTestCase
coverage report
```

### **Método 2: Script Interativo**
```bash
# Menu interativo
python executar_testes.py

# Executar todos os testes
python executar_testes.py todos

# Listar testes disponíveis
python executar_testes.py listar

# Executar teste específico
python executar_testes.py test_us7_listar_pedidos_aprovados
```

## 📊 Testes Disponíveis

### **Testes Funcionais**
1. `test_us7_listar_pedidos_aprovados` - Filtro de pedidos aprovados
2. `test_us7_programar_entrega_com_estoque_suficiente` - Programação com estoque
3. `test_us7_impedir_agendamento_estoque_insuficiente` - Validação de estoque
4. `test_us8_listar_entregas_hoje` - Filtro de entregas do dia
5. `test_us8_processar_entrega` - Processamento de entregas
6. `test_us9_relatorio_estoque_baixo` - Relatório de estoque baixo
7. `test_us9_relatorio_promocao` - Relatório de promoções
8. `test_us9_relatorio_por_grupo` - Relatório por grupos de preço
9. `test_us9_exportar_pdf` - Exportação em PDF
10. `test_us9_exportar_excel` - Exportação em Excel
11. `test_us9_pagina_principal_relatorios` - Página principal de relatórios

### **Testes de Segurança e Validação**
12. `test_acesso_sem_login` - Controle de acesso
13. `test_validacoes_negocio` - Regras de negócio
14. `test_calculo_valor_total` - Cálculos do sistema

## 🔧 Configuração dos Testes

### **Dados de Teste Criados Automaticamente:**
- **Usuário Gerente**: `gerente_teste` / `senha123`
- **Produtos**:
  - Notebook Dell (R$ 2.500,00, estoque: 20)
  - Mouse Logitech (R$ 45,00, estoque: 3)
  - Teclado Barato (R$ 25,00, estoque: 15)
  - Monitor (R$ 75,00, estoque: 8)
- **Cliente**: Cliente Teste (cliente@teste.com)

### **URLs Testadas:**
- `/venda/pedidos-aprovados/` - Listar pedidos aprovados
- `/venda/programar-entrega/<id>/` - Programar entrega
- `/venda/entregas-hoje/` - Entregas do dia
- `/venda/processar-entrega/<id>/` - Processar entrega
- `/venda/relatorios/` - Página principal de relatórios
- `/venda/relatorio/estoque-baixo/` - Relatório estoque baixo
- `/venda/relatorio/promocao/` - Relatório promoções
- `/venda/relatorio/por-grupo/` - Relatório por grupos
- `/venda/relatorio/pdf/<tipo>/` - Exportação PDF
- `/venda/relatorio/excel/<tipo>/` - Exportação Excel

## 📈 Relatório de Execução

O sistema de testes gera um relatório detalhado mostrando:
- ✅ Número total de testes executados
- ✅ Testes que passaram com sucesso
- ❌ Testes que falharam (se houver)
- 📊 Taxa de sucesso percentual
- 🎯 Status individual de cada teste

## 🚀 Exemplo de Saída

```
🧪 TESTANDO US7 - Listar Pedidos Aprovados
✅ Página de pedidos aprovados acessível
✅ Apenas pedidos APROVADOS são exibidos

🧪 TESTANDO US7 - Programar Entrega (Estoque Suficiente)
✅ Entrega programada e estoque subtraído automaticamente

📊 RELATÓRIO FINAL DA SUITE DE TESTES
═══════════════════════════════════════════════════════════════════════
📈 Total de testes executados: 14
✅ Testes com sucesso: 14
❌ Testes falharam: 0
📊 Taxa de sucesso: 100.0%

🎉 TODOS OS TESTES PASSARAM COM SUCESSO!
✅ User Stories 7, 8 e 9 estão funcionando corretamente
🚀 Sistema pronto para produção!
```

## 🛠️ Dependências

- Django 5.2.4
- reportlab (para exportação PDF)
- openpyxl (para exportação Excel)
- Python 3.13+

## 📝 Notas Importantes

1. **Banco de Dados**: Os testes usam um banco de dados temporário
2. **Isolamento**: Cada teste é executado de forma isolada
3. **Cleanup**: Dados são limpos automaticamente após cada teste
4. **Login**: Testes simulam login automático do gerente
5. **Validações**: Incluem verificações de status HTTP, conteúdo e regras de negócio

## 🔍 Troubleshooting

### Problema: Erro de migração
```bash
python manage.py makemigrations
python manage.py migrate
```

### Problema: Dependências ausentes
```bash
pip install reportlab openpyxl
```

### Problema: Permissões
- Certifique-se de que o usuário tem permissões adequadas
- Verifique se todas as views têm o decorator `@login_required`

---

**📞 Suporte**: Para dúvidas sobre os testes, consulte a documentação das views em `venda/views.py` ou execute `python executar_testes.py` para o menu interativo.

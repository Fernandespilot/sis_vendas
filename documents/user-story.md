# 📄 User Stories – Sistema de Gestão de Vendas

## 1. Promotor de vendas – Visualizar clientes
**Como** promotor de vendas  
**Quero** observar a lista de clientes a serem visitados na minha área de cobertura  
**Para** visitar esses clientes, divulgar os produtos e aumentar meu rendimento  

- Listagem por ordem alfabética, por rua e por status de visita (pendente/visitado)  
- Apenas clientes da área de cobertura atual ou do mês seguinte  
- Exibir nome, endereço completo e telefone  

---

## 2. Promotor de vendas – Registrar pedidos
**Como** promotor de vendas  
**Quero** registrar o pedido dos meus clientes  
**Para** realizar a venda de produtos e conseguir meu rendimento  

- Selecionar cliente existente ou cadastrar novo  
- Buscar produtos, informar quantidades, visualizar total e comissão estimada  
- Pedido salvo com mensagem de sucesso e status “pendente”  

---

## 3. Cliente – Acompanhar pedido
**Como** cliente  
**Quero** observar meu pedido feito pelo promotor de vendas  
**Para** checar e acompanhar o meu pedido  

- Visualizar código, data, lista de produtos, quantidades e valores  
- Acompanhar status (pendente, aprovado, em entrega, concluído)  
- Receber notificação por e-mail a cada mudança de status  

---

## 4. Gerenciador – Cadastrar promotor
**Como** gerenciador da empresa  
**Quero** cadastrar os promotores de venda  
**Para** manter seus dados pessoais e atribuir suas áreas de cobertura  

- Formulário com nome completo, CPF, telefone e e-mail  
- Seleção de ao menos uma região cadastrada  
- Mensagem de sucesso e listagem com cidades atribuídas  

---

## 5. Gerenciador – Cadastrar produtos
**Como** gerenciador da empresa  
**Quero** cadastrar os produtos que são vendidos na empresa  
**Para** divulgar os catálogos dos produtos  

- Campos obrigatórios: código, nome, grupo, custo, margem de lucro, estoque  
- Seleção de percentual de promoção e impostos aplicáveis  
- Produto aparece na lista com nome, grupo e estoque  

---

## 6. Gerente de estoque – Avaliar pedidos
**Como** gerente de estoque  
**Quero** avaliar os pedidos enviados pelos promotores  
**Para** verificar a existência dos produtos no estoque  

- Verificar código, data, cliente, produtos e quantidades  
- Estoque insuficiente é destacado em vermelho  
- Aprovar ou marcar como “Insuficiente”; status atualizado automaticamente  

---

## 7. Gerente de estoque – Programar entrega
**Como** gerente de estoque  
**Quero** avaliar os pedidos aprovados pelo gerente de vendas  
**Para** programar a data de entrega e reservar os produtos  

- Exibir somente pedidos com status “Aprovado”  
- Escolher data de entrega, subtrair estoque automaticamente  
- Impedir agendamento se houver falta de produto  
- Status atualizado para “Programado” com notificação ao cliente e promotor  

---

## 8. Gerente de estoque – Processar entrega
**Como** gerente de estoque  
**Quero** processar a entrega do pedido no dia marcado  
**Para** mudar o estado do pedido  

- Exibir somente pedidos com data de entrega igual ao dia atual  
- Botão “Processar entrega” altera status para “Processado”  
- Pedido sai da lista e aviso enviado ao cliente e promotor  

---

## 9. Gerente de estoque – Relatórios de produtos
**Como** gerente de estoque  
**Quero** emitir relatório dos produtos  
**Para** ter informações de estoque baixo, produtos em promoção e por grupo  

- Seleção do tipo de relatório desejado  
- Exibição de produto, estoque e preço  
- Download em PDF/Excel ou envio para impressão com confirmação  

---

## 10. Gerente de vendas – Analisar cliente
**Como** gerente de vendas  
**Quero** analisar as condições do cliente que fez um pedido  
**Para** confirmar o pedido (aprovar ou cancelar)  

- Visualizar código, nome/CNPJ, valor total, situação financeira  
- Botão “Aprovar” ou “Cancelar” (com justificativa obrigatória)  
- Status atualizado, com aviso ao promotor e gerente de estoque  

---

## 11. Gerente de vendas – Relatórios de vendas
**Como** gerente de vendas  
**Quero** emitir relatório de vendas  
**Para** acompanhar desempenho, comissões e regiões atendidas  

- Tipos: maiores compradores, por município, por promotor, por período  
- Relatórios com colunas de data, cliente, total, impostos, comissão  
- Download em PDF/Excel ou envio para impressão com mensagem de sucesso  
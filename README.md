# 🛠️ SisVenda - Sistema de Vendas

Este repositório contém a documentação e o desenvolvimento do sistema proposto na disciplina **Análise e Projeto de Sistemas Computacionais**, no período 2025/1.

## 📑 Índice

- [🏢 Visão Geral](#-visão-geral)
- [📘 User Stories](#-user-stories)
- [🧩 Modelo Conceitual DER](#-modelo-conceitual-der)
- [🔷 Modelo Conceitual Orientado a Objetos (OO)](#-modelo-conceitual-orientado-a-objetos-oo)
- [🗂️ Diagrama de Casos de Uso](#-diagrama-de-casos-de-uso)
- [📦 Pré-requisitos](#-pré-requisitos)
- [📝 Relatório de Testes](#-relatório-de-testes)

---
## 🏢 Visão Geral
A **Empresa X** atua no setor de vendas de materiais eletroeletrônicos por meio de **catálogos impressos**, distribuídos via correio com o apoio de uma equipe de **promotores de venda**. Esses promotores visitam clientes em suas respectivas **áreas de cobertura (municípios)** com o objetivo de divulgar produtos, registrar pedidos e, assim, aumentar suas comissões — calculadas com base no volume de compras dos clientes.

O sistema tem como objetivo **automatizar e gerenciar** esse processo, desde o **cadastro de promotores, clientes e produtos**, até o **registro, avaliação, entrega e acompanhamento de pedidos**. Ele também fornece **relatórios** para o controle de vendas, estoques e comissões.

A operação se dá da seguinte forma:

 1. **O promotor de vendas** visualiza sua lista de clientes, registra novos pedidos e acompanha suas comissões.

 2. **Os pedidos realizados** são enviados à empresa, onde passam por:
   - **Verificação de estoque** feita pelo gerente de estoque.
   - **Análise financeira do cliente** realizada pelo gerente de vendas, que aprova ou cancela o pedido.
   - Em caso de aprovação, é feita a **programação da entrega**, com reserva e baixa do estoque.
   - No dia da entrega, o pedido é **processado e finalizado**.

 3. **Os clientes** podem acompanhar seus pedidos e recebem notificações sobre o andamento.

 4. **Os gerentes de vendas e de estoque** têm acesso a **relatórios detalhados** para controle e tomada de decisões.
 
---
## 📘 User Stories

As histórias de usuário (User Stories) do sistema estão detalhadas no arquivo [user-storys.md](document/user-storys.md). Lá você encontrará a descrição completa das funcionalidades do sistema na perspectiva dos diferentes usuários:

- Promotor de vendas
- Cliente
- Gerenciador
- Gerente de estoque
- Gerente de vendas

---

## 🧩 Modelo Conceitual DER

```mermaid
erDiagram
    CLIENTE ||--o{ PEDIDO : FAZ
    CLIENTE }o--|| MUNICIPIO : RESIDE
    CLIENTE ||--|{ PROMOTOR_VENDA : ATENDIDO_POR
    PROMOTOR_VENDA ||--|{ MUNICIPIO : COBRE
    PROMOTOR_VENDA ||--o{ PEDIDO : REGISTRA
    PEDIDO ||--o{ ITEM_PEDIDO : CONTÉM
    ITEM_PEDIDO }|--|| PRODUTO : REFERE
    PRODUTO ||--|| GRUPO_PRODUTO : PERTENCE
```

### Modelo Lógico
![Diagrama Entidade Relacionamento Lógico](document/img/der-logico.jpg)

---

## 🔷 [Modelo Conceitual Orientado a Objetos (OO)](https://lucid.app/lucidchart/3ab6d960-81c9-46d6-b9e2-7b98e5dd0f45/edit?viewport_loc=-769%2C-109%2C3511%2C1748%2COaRhBAe6IYM9&invitationId=inv_eaf0bf03-8ad6-41cd-bfa8-1bc1b8b04ea0)

> Apresente o modelo conceitual orientado a objetos, com foco nas classes principais, atributos e relacionamentos.

### Pode incluir:
- Diagrama de classes UML (imagem)
- Descrição das classes e responsabilidades
- Heranças, associações e composições
- Comentários sobre a coesão e acoplamento

---

## 🗂️ Diagrama de Casos de Uso

> Apresente o(s) diagrama(s) de casos de uso que descrevem como os usuários interagem com o sistema.

### Sugestões:
- Inserir imagem dos casos de uso
- Listar os atores
- Descrever cada caso de uso brevemente (em formato de tabela ou lista)

---

## 📦 Pré-requisitos

Antes de começar, você vai precisar ter instalado:

- [Git](https://git-scm.com)
- [Python 3.x](https://www.python.org/)

---

## 📝 Relatório de Testes

O sistema inclui testes unitários completos para as User Stories 7, 8 e 9 relacionadas ao Gerente de Estoque.
Veja o relatório completo em [RELATORIO_TESTE_UNITARIO.md](RELATORIO_TESTE_UNITARIO.md)
- [pip](https://pip.pypa.io/en/stable/)

---

## 🚀 Como baixar o projeto

1. **Clone o repositório**
   ```bash
   git clone https://github.com/APS25-1/sisvenda.git
   ```
   
2. **Acesse a pasta do projeto**
   ```bash
   cd sisvenda
   ```

---

## ⚙️ Configuração

1. **Crie e ative um ambiente virtual**
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

---

## ▶️ Como rodar o projeto

1. **Execute as migrações**
   ```bash
   python manage.py migrate
   ```
2. **Crie um superusuário**
   ```bash
   python manage.py createsuperuser
   ```
3. **Inicie o servidor de desenvolvimento**
   ```bash
   python manage.py runserver
   ```
4. **Acesse no navegador**
   ```
   http://127.0.0.1:8000/
   ```

---

## 📝 Observações

- Certifique-se de estar na branch correta:
  ```bash
  git checkout dev
  ```
- Sempre ative o ambiente virtual antes de rodar comandos:
  ```bash
  venv\Scripts\activate
  ```

---

## � Testes Automatizados

### Testes do Gerente de Estoque (User Stories 7, 8 e 9)

Para executar os testes automatizados do módulo de Gerente de Estoque:

1. **Configure o ambiente de testes**
   ```bash
   python configurar_ambiente_teste.py
   ```

2. **Ative o ambiente virtual de teste**
   ```bash
   venv_teste\Scripts\activate
   ```

3. **Execute os testes**
   ```bash
   python gerar_relatorio_completo.py
   ```

4. **Relatórios disponíveis**
   - `RELATORIO_EXECUTIVO.md` - Resumo gerencial dos testes
   - `RELATORIO_TESTE_UNITARIO.md` - Detalhes técnicos completos
   - `output/*.png` - Gráficos e visualizações
   - `htmlcov/index.html` - Relatório de cobertura de código

Para mais informações, consulte o arquivo `TESTES_README.md`.

---

## �🤝 Contribuições

Contribuições são bem-vindas! Abra issues ou envie pull requests para melhorias.

---

Feito com ❤️ pela equipe APS25-1.
>>>>>>> feature/test-report

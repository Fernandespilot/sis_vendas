# Configuração do Projeto

- **Linguagem:** Python
- **Framework:** Django
- **Banco de Dados:** SQLite
- **Padrão de Arquitetura:** Model, View e Template (MVT)

---

## Camadas do Projeto

### 🔹 Camada Model:
- Responsável pela **lógica de dados** e pela **estrutura do banco de dados**.
- Define **como os dados são armazenados e recuperados**.
- Utiliza um **ORM (Object-Relational Mapping)** para interagir com o banco de dados, permitindo trabalhar com **objetos** em vez de escrever SQL diretamente.
- Cada **modelo** representa uma **tabela** no banco de dados.

---

### 🔹 Camada View:
- Processa as **requisições HTTP** e retorna **respostas** (geralmente em HTML).
- Recebe dados do **modelo** e os envia para a camada **Template**.
- Lida com a **lógica de negócios** relacionada às requisições.

---

### 🔹 Camada Template:
- Responsável por **formatar a resposta para o usuário**, geralmente em HTML.
- Recebe dados da **camada View** e gera a **página web**.
- Utiliza um **sistema de template** para criar a interface visual, permitindo que os desenvolvedores separem a **apresentação (HTML)** da **lógica de negócios**.

---

## Observações
- O Django utiliza o padrão **MVT** para organizar os projetos de forma clara e escalável.
- O **SQLite** é o banco de dados padrão do Django, ótimo para desenvolvimento e prototipagem.
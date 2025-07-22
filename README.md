# 🛠️ Projeto SISVENDA

Bem-vindo ao repositório do **SISVENDA**! Aqui você encontrará instruções para baixar, configurar e rodar o projeto localmente no Windows.

---

## 📦 Pré-requisitos

Antes de começar, você vai precisar ter instalado:

- [Git](https://git-scm.com)
- [Python 3.x](https://www.python.org/)
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

Mini ERP Comercial - FastAPI

Sistema ERP desenvolvido em Python com FastAPI para gerenciamento de clientes, produtos, vendas, estoque e pagamentos.

O projeto foi desenvolvido aplicando arquitetura em camadas, autenticação JWT, regras de negócio reais e testes automatizados com cobertura de 93%.

---

Sobre o Projeto

Este projeto é uma API ERP desenvolvida com FastAPI para gerenciamento de:

- Usuários
- Clientes
- Produtos
- Estoque
- Vendas
- Pagamentos
- Fechamento mensal

O sistema aplica autenticação JWT, arquitetura em camadas e testes automatizados para garantir segurança, organização e qualidade do código.

---

Tecnologias Utilizadas

- Python
- FastAPI
- SQL Server
- PyODBC
- JWT (python-jose)
- Passlib (bcrypt)
- Pytest
- Coverage.py
- Pydantic
- Uvicorn
- HTML
- Css
- JavaScript

---

Funcionalidades

Usuários

- Cadastro de usuários
- Login
- Autenticação JWT

Clientes

- Criar cliente
- Buscar cliente
- Atualizar cliente
- Inativar cliente
- Reativar cliente

Produtos

- Criar produto
- Buscar produto
- Atualizar produto
- Inativar produto
- Reativar produto
- Controle de estoque

Vendas

- Criar venda simples
- Criar venda completa
- Adicionar itens
- Atualizar itens
- Remover vendas pendentes

Pagamentos

- Pagamento parcial
- Pagamento total
- Controle de saldo

Fechamento Mensal

- Fechamento de vendas pagas
- Histórico de vendas fechadas

---

Segurança

- Senhas criptografadas com bcrypt
- Autenticação via JWT
- Proteção de rotas com token
- Isolamento de dados por usuário
- Tratamento centralizado de exceções

---

Testes Automatizados

O projeto possui:

- Testes unitários
- Testes de integração
- Testes de fluxo completo

Cobertura de Testes

- Cobertura total: 93%
- 1.787 linhas analisadas
- Fluxos principais totalmente testados

«Recomenda-se adicionar uma imagem do relatório HTML gerado pelo Coverage.py nesta seção.»

---

Estatísticas do Projeto

- Arquitetura em camadas
- Autenticação JWT
- CRUD completo de Clientes
- CRUD completo de Produtos
- Controle de Estoque
- Controle de Vendas
- Controle de Pagamentos
- Fechamento Mensal
- 93% de cobertura de testes

---

Como Executar o Projeto

1. Clone o repositório

https://github.com/lucasferreiramatos312-creator/mini-erp-comercial--fastapi.git

2. Instale as dependências

py -m pip install fastapi uvicorn pyodbc passlib[bcrypt] python-jose pytest pytest-cov

3. Configure o Banco de Dados

- Crie o banco de dados no SQL Server.
- Ajuste a string de conexão no arquivo "database.py".

4. Execute o Servidor

uvicorn main:app --reload

5. Acesse a Documentação

http://127.0.0.1:8000/docs

6. Frontend

Abra o arquivo "index.html" utilizando a extensão Live Server.

---

Arquitetura do Projeto

O projeto segue o padrão de separação em camadas:

Routes        → Entrada da API (HTTP)
Services      → Regras de negócio
Repositories  → Acesso ao banco de dados
Security      → Autenticação e criptografia
Models        → Estruturas de dados
Tests         → Testes automatizados

Essa estrutura facilita manutenção, escalabilidade e organização do código.

---

Aprendizados

Durante o desenvolvimento deste projeto foram aplicados conceitos como:

- Arquitetura em camadas
- Autenticação JWT
- Integração Backend + Frontend
- Testes automatizados
- Cobertura de código
- Tratamento de exceções
- Regras de negócio
- Consumo de API com JavaScript
- Integração com SQL Server

---

## Imagens do Projeto

### Documentação Swagger

![Swagger](images/swagger.png)
![Swagger](images/swagger2.png)
### Cobertura de Testes

![Coverage](images/coverage.png)
![Coverage](images/coverage2.png)

Melhorias Futuras

- Dashboard financeiro melhorado 
- Relatórios PDF
- Docker
- Deploy em nuvem
- React no frontend
- Controle de usuários por perfil
- Exportação para Excel
- Dashboard administrativo

---

Autor

Lucas Ferreira

Desenvolvedor Backend Python
[18:25, 30/06/2026] Lucas: Primeira versão estável do Mini ERP Comercial.

Funcionalidades:
- Gestão de clientes
- Gestão de produtos
- Controle de estoque
- Controle de vendas
- Controle de pagamentos
- Dashboard administrativo
- Autenticação JWT
- Soft Delete
- Docker
- Deploy Backend
- Deploy Frontend
- Testes automatizados com 93% de cobertura

Tecnologias:
Python, FastAPI, SQL Server, HTML, CSS, JavaScript, Docker e Render.
[18:25, 30/06/2026] Lucas: git add .
git commit -m "feat: release final Mini ERP Comercial v1.0"
git push origin main

git tag -a v1.0.0 -m "Primeira versão estável do Mini ERP Comercial"
git push origin v1.0.0
[18:32, 30/06/2026] Lucas: https://mini-erp-comercial-frontend.onrender.com/login.html
[18:32, 30/06/2026] Lucas: Mini ERP Comercial | FastAPI | SQL Server → PostgreSQL

Sistema ERP Comercial desenvolvido em Python com FastAPI para gerenciamento de clientes, produtos, estoque, vendas e pagamentos.

O projeto foi criado a partir de uma necessidade real de negócio e desenvolvido aplicando arquitetura em camadas, autenticação JWT, testes automatizados, containerização com Docker, migração de banco de dados e deploy em nuvem.

---

Demonstração

Aplicação Online

Frontend

https://mini-erp-comercial-frontend.onrender.com/login.html

Backend (API)

https://mini-erp-comercial-fastapi.onrender.com

Documentação Swagger

https://mini-erp-comercial-fastapi.onrender.com/docs

---

Sobre o Projeto

O Mini ERP Comercial é um sistema completo para gestão comercial que permite controlar:

- Usuários
- Clientes
- Produtos
- Estoque
- Vendas
- Pagamentos
- Fechamento mensal

O sistema foi desenvolvido utilizando arquitetura em camadas, separando responsabilidades entre rotas, regras de negócio e acesso aos dados, facilitando manutenção, escalabilidade e evolução futura.

Inicialmente o projeto foi desenvolvido utilizando SQL Server durante o ambiente de desenvolvimento local. Posteriormente foi realizada uma migração completa para PostgreSQL visando compatibilidade com o ambiente de produção e deploy na nuvem utilizando Render.

---

Tecnologias Utilizadas

Backend

- Python
- FastAPI
- SQL Server (Desenvolvimento)
- PostgreSQL (Produção)
- PyODBC
- Psycopg
- Pydantic
- JWT (python-jose)
- Passlib (bcrypt)
- Uvicorn

Frontend

- HTML5
- CSS3
- JavaScript

Testes

- Pytest
- Coverage.py

DevOps

- Docker
- Git
- GitHub
- Render

Ambiente

- Linux
- WSL (Windows Subsystem for Linux)

---

Funcionalidades

Usuários

- Cadastro de usuários
- Login
- Autenticação JWT
- Proteção de rotas

Clientes

- Cadastro
- Consulta
- Atualização
- Inativação (Soft Delete)
- Reativação

Produtos

- Cadastro
- Consulta
- Atualização
- Controle de estoque
- Inativação (Soft Delete)
- Reativação

Vendas

- Criação de vendas
- Adição de múltiplos itens
- Atualização de itens
- Exclusão de vendas pendentes
- Cálculo automático de total

Pagamentos

- Pagamento parcial
- Pagamento total
- Controle de saldo pendente
- Atualização automática do status da venda

Fechamento Mensal

- Fechamento de vendas pagas
- Histórico de vendas fechadas

Dashboard

- Total de vendas
- Faturamento
- Valores recebidos
- Valores pendentes
- Quantidade de clientes
- Quantidade de produtos
- Ticket médio

---

Segurança

- Senhas criptografadas com bcrypt
- Autenticação JWT
- Proteção de endpoints
- Isolamento de dados por usuário
- Tratamento centralizado de exceções
- Validação de regras de negócio

---

Arquitetura do Projeto

Routes
│
├── Services
│
├── Repositories
│
├── Security
│
├── Models
│
└── Tests

Responsabilidades

Routes

Recebimento das requisições HTTP.

Services

Implementação das regras de negócio.

Repositories

Acesso e manipulação dos dados no banco.

Security

Autenticação e criptografia.

Models

Estruturas e validações de dados.

Tests

Testes automatizados da aplicação.

---

Testes Automatizados

O projeto possui:

- Testes unitários
- Testes de integração
- Testes de fluxo completo

Cobertura

- Cobertura total: 93%
- Mais de 1.700 linhas analisadas
- Principais fluxos totalmente testados

---

Docker e Deploy

O projeto foi containerizado utilizando Docker para garantir consistência entre ambientes de desenvolvimento e produção.

Implementações

- Dockerfile para Backend
- Containerização da aplicação
- Configuração para deploy em nuvem
- Deploy do Backend no Render
- Deploy do Frontend no Render
- Migração SQL Server → PostgreSQL
- Configuração de banco PostgreSQL em produção

Benefícios

- Ambiente padronizado
- Facilidade de implantação
- Escalabilidade
- Independência de dependências locais

---

Principais Desafios Técnicos

Migração de Banco de Dados

O projeto foi originalmente desenvolvido utilizando SQL Server e posteriormente migrado para PostgreSQL para viabilizar o deploy em produção.

Durante a migração foram realizados:

- Conversão de consultas SQL
- Adaptação de tipos de dados
- Ajustes de compatibilidade
- Testes de integridade
- Validação das regras de negócio

---

Soft Delete

Implementação de exclusão lógica para clientes e produtos, preservando histórico e integridade dos dados.

---

Refatoração da API

Padronização das respostas da aplicação:

{
  "sucesso": true,
  "dados": {},
  "mensagem": "Operação realizada com sucesso"
}

---

Controle Dinâmico de Status

O status das vendas é calculado automaticamente a partir dos pagamentos registrados:

- PENDENTE
- PARCIAL
- PAGO
- FECHADA

---

Estatísticas do Projeto

- Mais de 30 endpoints implementados
- Backend + Frontend integrados
- Autenticação JWT
- Controle de estoque
- Controle financeiro
- Dashboard administrativo
- Soft Delete
- Migração SQL Server → PostgreSQL
- Docker
- Deploy em nuvem
- 93% de cobertura de testes

---

Aprendizados

Durante o desenvolvimento deste projeto foram aplicados conceitos de:

- Desenvolvimento Backend
- APIs REST
- Arquitetura em Camadas
- Programação Orientada a Objetos
- SQL Server
- PostgreSQL
- Migração de bancos relacionais
- Modelagem de Dados
- Soft Delete
- Autenticação JWT
- Testes Automatizados
- Docker
- Deploy
- Integração Backend + Frontend
- Git e GitHub
- Linux e WSL

---

Melhorias Futuras

- Relatórios PDF
- Exportação para Excel
- Controle de permissões por perfil
- Dashboard avançado
- React no Frontend
- Integração com WhatsApp
- Módulo de relatórios gerenciais
- Integração com Inteligência Artificial

---

Autor

Lucas Ferreira

Estudante de Desenvolvimento de Sistemas | Desenvolvedor Backend Python

GitHub:
https://github.com/lucasferreiramatos312-creator

LinkedIn:
https://www.linkedin.com/in/lucas-ferreira-991b093a0
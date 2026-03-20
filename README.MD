Sistema de Produtos com Autenticação (FastAPI)

Sistema backend completo com autenticação JWT e controle de acesso por usuário.

---

## Sobre o projeto

Este projeto é uma API desenvolvida com FastAPI que permite:

- Cadastro de usuários
- Login com autenticação JWT
- CRUD completo de produtos
- Cada usuário acessa apenas seus próprios dados

---

## Tecnologias utilizadas

- Python
- FastAPI
- SQL Server
- PyODBC
- JWT (python-jose)
- Passlib (bcrypt)
- HTML + JavaScript (frontend simples)

---

## Funcionalidades

### Usuários
- Criar usuário (POST /auth/registrar)
- Login (POST /auth/login)

### Produtos
- Listar produtos do usuário logado (GET /api/produtos)
- Buscar produto por ID (GET /api/produtos/{id})
- Criar produto (POST /api/produtos)
- Atualizar produto (PUT /api/produtos/{id})
- Deletar produto (DELETE /api/produtos/{id})

---

##  Segurança

- Senhas criptografadas com bcrypt
- Autenticação via JWT
- Proteção de rotas com token
- Isolamento de dados por usuário

---

## Como executar o projeto

### 1. Clone o repositório
```bash
git clone https://github.com/lucasferreiramatos312-creator

2. Instale as dependências
Bash
py -m pip install fastapi uvicorn pyodbc passlib[bcrypt] python-jose

3. Configure o banco de dados
Crie o banco no SQL Server
Ajuste a string de conexão no arquivo database.py

4. Execute o servidor
Bash
uvicorn main:app --reload

5. Acesse a documentação

http://127.0.0.1:8000/docs
6. Frontend

Abra o arquivo index.html com a extensão Live Server

 Arquitetura do projeto:

O projeto segue o padrão de separação em camadas:
Routes → Entrada da API (HTTP)
Services → Regras de negócio
Repositories → Acesso ao banco de dados
Security → Autenticação e criptografia
Essa estrutura facilita manutenção, escalabilidade e organização do código.

Aprendizados:
Durante o desenvolvimento deste projeto foram aplicados conceitos como:
Arquitetura em camadas
Autenticação com JWT
Integração backend + frontend
Debug e tratamento de erros
Consumo de API com JavaScript

Melhorias futuras:
Interface com React
Deploy em nuvem
Docker
Testes automatizados
Refresh Token
 
Autor: Lucas Ferreira:
Desenvolvedor Backend Python
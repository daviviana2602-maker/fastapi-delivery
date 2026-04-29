# 🍔 Delivery API — Backend com FastAPI

API REST completa de um sistema de delivery desenvolvida com **Python + FastAPI + PostgreSQL**, focada em **autenticação segura**, **gestão de pedidos**, **controle administrativo de usuários**, **garantia de qualidade** e **boas práticas de arquitetura backend**.

Projeto backend completo simulando operação real de delivery com autenticação, pedidos, administração e testes automatizados.

---

# 📌 Visão Geral

Este projeto demonstra conhecimento em:

- Desenvolvimento de APIs REST profissionais  
- Arquitetura modular e escalável  
- Autenticação com JWT  
- Regras de negócio e permissões  
- Integração com banco relacional  
- Testes automatizados com Pytest  
- Containers com Docker  
- Versionamento de banco com Alembic  

---

# 🚀 Stack Tecnológica

## Backend

- Python 3.11+
- FastAPI
- SQLAlchemy ORM
- Pydantic

## Banco de Dados

- PostgreSQL

## Segurança

- JWT (`python-jose`)
- Hash de senha com Argon2 (`passlib`)

## Testes

- Pytest
- FastAPI TestClient

## DevOps

- Docker
- Docker Compose
- Dotenv

## Migrações

- Alembic

---

# ⚙️ Funcionalidades

## 🔐 Autenticação

- Criar conta
- Login com JWT
- Refresh token
- Proteção de rotas autenticadas
- Hash seguro de senha com Argon2

## 👤 Perfil do Usuário

- Atualizar nome
- Atualizar email
- Alterar senha validando senha atual
- Excluir conta também validando senha atual

## 🛒 Sistema de Pedidos

- Criar pedido
- Adicionar itens
- Alterar quantidade
- Checar itens no pedido até o momento
- Concluir pedido
- Cancelar pedido
- Consultar pedidos por status (admin)

## 🍽️ Cardápio

- Banco populado automaticamente com itens iniciais
- Estrutura pronta para expansão

## 🛡️ Administração

- Promover usuário para admin
- Rebaixar admin
- Desativar usuário
- Reativar usuário
- Controle por permissões

---

# 🧠 Arquitetura do Projeto

Estrutura organizada em camadas para facilitar manutenção e crescimento:

    .
    ├── alembic/
    ├── db/
    ├── routes/
    ├── services/
    ├── tests/
    ├── .env
    ├── .env.tests
    ├── Dockerfile
    ├── docker-compose.yml
    ├── alembic.ini
    ├── config.py
    ├── dependencies.py
    ├── helpers.py
    ├── main.py
    ├── response_schemas.py
    ├── schemas.py
    ├── security.py
    ├── token_utils.py
    └── README.md

## 📂 Responsabilidades

**routes/**  
Responsável pelas rotas HTTP da aplicação.

**services/**  
Contém regras de negócio desacopladas das rotas.

**db/**  
Models, conexão e estrutura do banco.

**tests/**  
Testes automatizados cobrindo fluxos principais.

**dependencies.py**  
Injeção de dependências como autenticação e sessão do banco.

---

# 🗄️ Banco de Dados

O projeto utiliza duas bases separadas.

## Ambiente principal

Usado via Docker Compose:

    DATABASE_URL=postgresql+psycopg2://postgres:senhaaqui@db...

## Ambiente de testes

Banco isolado para execução de testes automatizados:

    TEST_DATABASE_URL=postgresql+psycopg2://postgres:senhaaqui@localhost:...

Isso garante independência entre desenvolvimento e testes.

---

# 🔄 Migrações com Alembic

Controle de versionamento do schema:

    alembic revision --autogenerate -m "mensagem"
    alembic upgrade head
    alembic downgrade -1

---

# 🧪 Testes Automatizados

Projeto validado com Pytest cobrindo fluxos reais da aplicação.

## Exemplos testados

- Criação de conta  
- Login  
- Autenticação JWT  
- Atualização de perfil  
- Criação de pedidos  
- Alterações administrativas  
- Regras de permissão  
- Fluxos inválidos  

## Resultado atual

    22 passed (tudo funcionando como o esperado)

---

# 🐳 Como Rodar com Docker

## 1. Clonar projeto

    git clone https://github.com/daviviana2602-maker/fastapi-delivery.git
    cd fastapi-delivery

## 2. Criar arquivo `.env`

    DATABASE_URL=postgresql+psycopg2://postgres:senha@db:5432/delivery_db
    SECRET_KEY=sua_chave_secreta
    ALGORITHM=HS256
    ACCESS_TOKEN_EXPIRE_MINUTES=30

## 3. Subir containers

    docker compose up --build

## 4. Acessar API

Swagger:

    http://127.0.0.1:8000/docs

ReDoc:

    http://127.0.0.1:8000/redoc

---

# 📈 Diferenciais Técnicos

- Arquitetura organizada por responsabilidades  
- Regras de negócio separadas das rotas  
- Testes automatizados reais  
- Banco isolado para testes  
- JWT implementado corretamente  
- Hash seguro com Argon2  
- Docker para ambiente reproduzível  
- Alembic para versionamento do banco  

---

# 🎯 Objetivo do Projeto

Demonstrar capacidade prática para atuar em vagas de:

- Estágio Backend  
- Desenvolvedor Backend Júnior  
- QA Automation com Python  
- Suporte técnico com foco em APIs  

---

# 👨‍💻 Autor

**Davi Viana**

Desenvolvedor focado em backend com Python, APIs REST e bancos relacionais.

GitHub: https://github.com/daviviana2602-maker  
LinkedIn: https://www.linkedin.com/in/davi-viana-34a19b300/

---

# 📌 Status Atual

- ✅ Projeto funcional  
- ✅ API completa  
- ✅ Testes automatizados  
- ✅ Docker funcionando  
- ✅ PostgreSQL integrado  
- ✅ JWT implementado  
- ✅ Estrutura escalável  
- ✅ Em evolução constante
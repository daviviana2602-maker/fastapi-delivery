# 🍔 Delivery API — Fullstack Backend + Frontend (FastAPI)

API REST completa de um sistema de delivery desenvolvida com **Python + FastAPI + PostgreSQL**, incluindo **frontend básico (HTML/CSS/JS)** para consumo da API.

Projeto simula um sistema real de delivery com autenticação, pedidos, administração de usuários, regras de negócio e testes automatizados.

---

# 📌 Visão Geral

Este projeto demonstra experiência prática em:

- APIs REST profissionais com FastAPI  
- Arquitetura backend escalável  
- Autenticação JWT segura  
- Controle de permissões (RBAC)  
- Banco de dados relacional PostgreSQL  
- ORM com SQLAlchemy  
- Migrações com Alembic  
- Testes automatizados com Pytest  
- Containerização com Docker  
- Integração backend + frontend simples  

---

# 🚀 Stack Tecnológica

## Backend
- Python 3.11+
- FastAPI
- SQLAlchemy
- Pydantic

## Banco de Dados
- PostgreSQL

## Segurança
- JWT (python-jose)
- Hash de senha com Argon2

## Testes
- Pytest
- FastAPI TestClient

## DevOps
- Docker
- Docker Compose
- dotenv

## Frontend (básico)
- HTML5
- CSS3
- JavaScript (Fetch API)

## Migrações
- Alembic

---

# ⚙️ Funcionalidades

## 🔐 Autenticação
- Criar conta
- Login com JWT
- Proteção de rotas
- Hash seguro de senha

## 👤 Perfil
- Atualizar dados do usuário
- Alterar senha
- Excluir conta

## 🛒 Pedidos
- Criar pedidos
- Adicionar itens
- Concluir pedido
- Cancelar pedido
- Consultar status

## 🛡️ Administração
- Promover usuário
- Rebaixar usuário
- Desativar usuário
- Reativar usuário

## 🍽️ Cardápio
- Itens iniciais automatizados
- Estrutura pronta para expansão

---

# 🧠 Arquitetura


.
├── alembic/
├── db/
├── routes/
├── services/
├── tests/
├── frontend/
│ ├── html/
│ ├── css/
│ └── js/
├── main.py
├── schemas.py
├── dependencies.py
├── security.py
├── docker-compose.yml
└── Dockerfile


---

# 🌐 Frontend (Simples)

Frontend estático desenvolvido apenas para consumo da API.

## 🚀 Como rodar o frontend

No terminal:
cd frontend
python -m http.server 5500

Acesse no navegador:

http://localhost:5500/html/login.html

## ⚙️ Funcionalidades do Frontend

Login com JWT (armazenado no localStorage)
Registro de usuário
Painel administrativo (CRUD de usuários)
Consumo da API via Fetch
Proteção simples de rotas via auth guard

---

# 🔗 Integração com API

O frontend consome o backend rodando em:

http://localhost:8000

Fluxo completo:

Subir backend:
docker compose up --build
Subir frontend:
python -m http.server 5500
Acessar no navegador

---

# 🗄️ Banco de Dados

## Produção (Docker)


DATABASE_URL=postgresql+psycopg2://postgres:senha@db:5432/delivery_db


## Testes


TEST_DATABASE_URL=postgresql+psycopg2://postgres:senha@localhost:5432/test_db


---

# 🔄 Alembic


alembic revision --autogenerate -m "message"
alembic upgrade head
alembic downgrade -1


---

# 🧪 Testes

- Fluxos completos de autenticação
- CRUD de usuários
- Regras de permissão
- Pedidos e status
- Validação de erros

✔ 23 testes passando

---

# 🐳 Como Rodar

## 1. Clonar projeto


git clone https://github.com/daviviana2602-maker/fastapi-delivery.git

cd fastapi-delivery


## 2. Configurar .env


DATABASE_URL=postgresql+psycopg2://postgres:senha@db:5432/delivery_db
SECRET_KEY=sua_chave
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30


## 3. Subir projeto


docker compose up --build


---

# 🌐 Rodar Frontend

Abra o arquivo:


frontend/html/login.html


ou qualquer página HTML diretamente no navegador.

---

# 📍 API

- Swagger: http://localhost:8000/docs  
- ReDoc: http://localhost:8000/redoc  

---

# 📈 Diferenciais

- API real com regras de negócio
- Arquitetura modular
- Segurança com JWT + hash
- Frontend funcional integrado
- Testes automatizados reais
- Docker pronto para produção

---

# 🎯 Objetivo

Projeto criado para demonstrar habilidades em:

- Backend Python profissional
- APIs reais com FastAPI
- Integração fullstack básica
- Boas práticas de engenharia de software

---

# 👨‍💻 Autor

**Davi Viana**

- GitHub: https://github.com/daviviana2602-maker  
- LinkedIn: https://www.linkedin.com/in/davi-viana-34a19b300/
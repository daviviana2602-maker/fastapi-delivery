# 🍔 Delivery API — FastAPI Fullstack Project

Sistema de delivery fullstack desenvolvido com FastAPI, PostgreSQL e frontend funcional em HTML/CSS/JS. Simula um ambiente real de produção com autenticação JWT, regras de negócio, controle de acesso e deploy em cloud.

---

# 📌 Visão Geral

API REST profissional com autenticação, RBAC, CRUD completo de usuários e pedidos, integração com frontend estático e deploy em produção.

---

# ⚙️ Stack

Backend: Python 3.11+, FastAPI, SQLAlchemy, Pydantic  
Banco: PostgreSQL  
Auth: JWT (python-jose) + Argon2  
Testes: Pytest  
DevOps: Docker, Docker Compose  
Frontend: HTML, CSS, JS (Fetch API)
Deploy: Railway, Vercel, Supabase

---

# 🚀 Funcionalidades

- Login e cadastro com JWT
- Controle de acesso (admin / user)
- CRUD de usuários
- Sistema de pedidos completo
- Alteração de status de pedidos
- Painel administrativo
- Proteção de rotas
- Integração backend + frontend

---

# 🧠 Estrutura

.
├── alembic
├── db
├── routes
├── services
├── tests
├── front
│   ├── pages
│   ├── css
│   └── js
├── alembic.ini
├── config.py
├── dependencies.py
├── docker-compose.yml
├── Dockerfile
└── helpers.py
├── main.py
├── requirements.txt
├── response_schemas.py
├── schemas.py
├── security.py
└── token_utils

---

# 🌐 Frontend

Frontend estático que consome a API.

Rodar local:

cd frontend  
python -m http.server 5500  

Acesso:

http://localhost:5500/pages/login.html

---

# 🔗 API

Local:

http://localhost:8000  

Docs:

- Swagger: /docs  
- ReDoc: /redoc  

---

# 🗄️ Banco de Dados

Produção (Docker):

DATABASE_URL=postgresql+psycopg2://postgres:senha@db:5432/delivery_db  

Testes:

TEST_DATABASE_URL=postgresql+psycopg2://postgres:senha@localhost:5432/test_db  

---

# 🔄 Migrações

alembic revision --autogenerate -m "message"  
alembic upgrade head  
alembic downgrade -1  

---

# 🧪 Testes

- Autenticação JWT
- CRUD de usuários
- Regras de permissão
- Fluxo de pedidos

✔ 23 testes passando

pytest  

---

# 🐳 Docker

docker compose up --build   # inicia o projeto
docker compose down         # encerra os containers

---

# 🚀 Deploy

## Backend (Railway)

API hospedada em produção via Railway.

URL:

https://fastapi-delivery-production.up.railway.app  

Variáveis de ambiente configuradas no deploy:

- DATABASE_URL
- SECRET_KEY
- ALGORITHM
- ACCESS_TOKEN_EXPIRE_MINUTES

---

## Frontend (Vercel / Static Hosting)

Frontend pode ser deployado separadamente como site estático.

Configuração:

- Build: não necessário
- Root: /frontend/html
- API_BASE apontando para backend em produção

Exemplo:

const API_BASE = "https://fastapi-delivery-production.up.railway.app"

---

## Fluxo de deploy

1. Backend sobe no Railway (Docker + env vars)
2. Frontend sobe na Vercel
3. Frontend consome API remota
4. JWT autentica usuário em produção

---

# 📈 Destaques

- API real com regras de negócio
- Arquitetura modular
- JWT + segurança de senha
- Frontend funcional integrado
- Testes automatizados
- Deploy separado frontend/backend
- Pronto para produção

---

# 🎯 Objetivo

Demonstrar domínio em backend profissional com Python, criação de APIs reais com FastAPI, integração fullstack e deploy em cloud.

---

# 👨‍💻 Autor

Davi Viana  
GitHub: https://github.com/daviviana2602-maker  
LinkedIn: https://www.linkedin.com/in/davi-viana-34a19b300/
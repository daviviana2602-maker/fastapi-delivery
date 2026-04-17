# 🍔 Delivery API - Backend (FastAPI)

API completa de um sistema de delivery desenvolvida com **Python + FastAPI + PostgreSQL**, focada em autenticação, controle de pedidos e administração de usuários.

Projeto criado como forma de estudo prático de backend moderno, arquitetura de APIs e boas práticas com Python.

---

## 🚀 Tecnologias utilizadas

- Python 3.11+
- FastAPI
- SQLAlchemy
- PostgreSQL
- JWT (python-jose)
- Passlib (argon2)
- Pydantic
- Uvicorn
- Dotenv
- Alembic
- Docker

---

## ⚙️ Funcionalidades

### 🔐 Autenticação
- Criar conta
- Login com JWT
- Refresh token
- Senhas criptografadas (argon2)

### 👤 Perfil de usuário
- Atualizar nome, email e senha
- Validação de senha atual para segurança

### 🛒 Sistema de pedidos
- Criar pedido
- Adicionar itens temporários (carrinho)
- Ajustar quantidade de itens
- Finalizar pedido
- Cancelar pedido
- Listar pedidos por status

### 🍽️ Cardápio
- Itens pré-populados automaticamente no banco

### 🛡️ Administração
- Promover usuários a admin
- Rebaixar admin
- Desativar / reativar usuários
- Controle de permissões (admin / dono do recurso)

---

## 🧠 Arquitetura do projeto

O projeto segue uma estrutura modular baseada em:

- Routes (controllers)
- Models (SQLAlchemy)
- Schemas (Pydantic)
- Dependencies (auth e DB session)
- Helpers (funções auxiliares)
- Security (hash de senha)
- Token utils (JWT)

---

## 🗄️ Controle de Migrações (Alembic)

O projeto utiliza **Alembic** para versionamento do banco de dados PostgreSQL.

Isso permite evoluir o schema do banco de forma segura durante o desenvolvimento, sem precisar apagar tabelas manualmente.

---

### ⚙️ Fluxo básico de uso

```bash
# inicializa alembic (uma vez)
python -m alembic init alembic

# cria migration automática
python -m alembic revision --autogenerate -m "mensagem"

# aplica migrations
python -m alembic upgrade head

# rollback
python -m alembic downgrade <revision_id>

# reset completo (DEV apenas)
python -m alembic downgrade base
python -m alembic upgrade head
```

---

## 📁 Estrutura do projeto

```
.
├── auth_routes.py
├── order_routes.py
├── profile_routes.py
├── management_routes.py
├── models.py
├── schemas.py
├── response_schemas.py
├── dependencies.py
├── helpers.py
├── security.py
├── token_utils.py
├── config.py
├── populate_db.py
├── main.py
└── tests/
```

---

## ▶️ Como rodar o projeto

### 1. Clonar repositório
```bash
git clone https://github.com/daviviana2602-maker/fastapi-delivery.git
cd fastapi-delivery
```

### 2. Criar ambiente virtual
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar variáveis de ambiente

Crie um arquivo `.env`:

```env
DATABASE_URL=postgresql+psycopg2://postgres:senha@db:5432/delivery_db
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

### 5. Rodar com Docker (recomendado)

```bash
docker compose up --build
```

---

### 6. Rodar local (sem Docker)

```bash
uvicorn main:app --reload
```

---

## 📌 Observações

- O primeiro usuário criado vira **admin automaticamente**
- Cardápio é populado automaticamente ao iniciar
- API disponível em:
```
http://127.0.0.1:8000/docs    (Swagger UI)
```

---

## 🧪 Testes

O projeto inclui testes em JavaScript usando `fetch` para simular requisições de frontend.

---

## 📈 Objetivo do projeto

Este projeto foi desenvolvido com foco em:

- prática real de backend
- arquitetura de APIs profissionais
- autenticação JWT
- controle de permissões
- estrutura escalável

---

## 👨‍💻 Autor

**Davi**

Backend developer em evolução — Python, APIs, sistemas escaláveis.

---

## 📌 Status

✔️ Projeto funcional  
✔️ API testada via Swagger e JS  
✔️ Banco PostgreSQL integrado  
✔️ Docker funcionando  
✔️ Autenticação completa
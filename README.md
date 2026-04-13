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

## 📁 Estrutura

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
└── tests/ (requests em JS)
```

---

## ▶️ Como rodar o projeto

### 1. Clonar repositório
```bash
git clone https://github.com/seu-usuario/delivery-api.git
cd delivery-api
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

```
DATABASE_URL=sua_url_do_postgres
SECRET_KEY=sua_chave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 5. Rodar servidor

```bash
uvicorn main:app --reload
```

---

## 📌 Observações

- O primeiro usuário criado automaticamente vira **admin**
- O sistema já inicia com cardápio populado automaticamente
- Todas as rotas são testáveis via Swagger:

```
http://127.0.0.1:8000/docs
```

---

## 🧪 Testes

O projeto inclui arquivos de teste em JavaScript usando `fetch` para simular requisições de frontend.

---

## 📈 Objetivo do projeto

Este projeto foi desenvolvido com foco em:

- Prática real de backend
- Estruturação de APIs profissionais
- Autenticação segura com JWT
- Controle de permissões
- Organização de código escalável

---

## 👨‍💻 Autor

Desenvolvido por **Davi**  
Estudando backend com foco em Python, APIs e sistemas escaláveis.

---

## 📌 Status

✔️ Projeto funcional  
✔️ APIs testadas via Swagger e scripts JS  
✔️ Banco integrado com PostgreSQL  
✔️ Segurança com JWT + hashing  
```
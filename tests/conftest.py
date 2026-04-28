import pytest
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from db.models import Base, UserTable
from main import app
from dependencies import get_db
from populate_test_db import popular_db_teste
from security import argon_context
import uuid


# carrega ambiente de teste
load_dotenv(".env.tests", override=True)    # se já existir variável carregada antes, substitui
TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")


engine = create_engine(TEST_DATABASE_URL,)

TestingSessionLocal = sessionmaker(bind=engine)



@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # limpa tudo antes de começar
    Base.metadata.drop_all(bind=engine)

    # recria tabelas
    Base.metadata.create_all(bind=engine)
    popular_db_teste()
    


# entrega uma sessão do banco pronta para cada teste
@pytest.fixture(scope="function")
def db():
    connection = engine.connect()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        connection.close()



@pytest.fixture(scope="function")
def api_client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db  # Sempre que alguma rota pedir get_db, use override_get_db

    client = TestClient(app)

    yield client

    app.dependency_overrides.clear()   # Limpa configuração em memória e evita que um teste afete outro
    
    
    
@pytest.fixture
def user_alvo(api_client):
    res = api_client.post(
        "/auth/criar_conta",
        json={
            "nome": "User teste",
            "email": f"user_{uuid.uuid4()}@test.com",   # gera email diferente toda vez com uuid
            "senha": "123456"
        }
    )

    return res.json()["data"]["id"]



# cria usuário admin para testes que precisem
@pytest.fixture
def admin_user(db):
    admin = db.query(UserTable).filter_by(email="admin@test.com").first()

    if not admin:
        admin = UserTable(
            nome="admin",
            email="admin@test.com",
            senha=argon_context.hash("123456"),
            admin=True,
            ativo=True
        )

        db.add(admin)
        db.commit()
        db.refresh(admin)

    return admin



# faz login como admin e pega o access token gerado
@pytest.fixture
def admin_token(api_client, admin_user):
    res = api_client.post(
        "/auth/login",
        json={
            "email": admin_user.email,
            "senha": "123456"
        }
    )

    return res.json()["data"]["access_token"]



# passa o token admin como header para passar da dependencie checar_admin das rotas management
@pytest.fixture
def admin_headers(admin_token):
    return {"Authorization": f"Bearer {admin_token}"}
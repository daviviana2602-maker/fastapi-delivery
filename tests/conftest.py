import pytest
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from db.models import UserTable, OrderTable, CardapioTable, ExcludedUserTable, TempItemsTable, CompletedOrderItem
from db.models import Base
from main import app
from dependencies import get_db


# carrega ambiente de teste
load_dotenv(".env.tests", override=True)

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_engine(
    TEST_DATABASE_URL,
    echo=True,
    pool_pre_ping=True
)

print("DB URL REAL:", TEST_DATABASE_URL)
print("ENGINE URL:", engine.url)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# 🔥 RESET TOTAL DO BANCO (ANTES E DEPOIS DOS TESTES)
@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # limpa tudo antes de começar
    Base.metadata.drop_all(bind=engine)

    # recria tabelas
    Base.metadata.create_all(bind=engine)


# 🔥 sessão REAL (sem rollback escondido)
@pytest.fixture(scope="function")
def db():
    connection = engine.connect()
    session = TestingSessionLocal(bind=connection)

    try:
        yield session
    finally:
        session.close()
        connection.close()


# 🔥 override do FastAPI dependency
@pytest.fixture(scope="function")
def api_client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)

    yield client

    app.dependency_overrides.clear()
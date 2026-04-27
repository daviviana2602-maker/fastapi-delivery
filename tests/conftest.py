import pytest
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fastapi.testclient import TestClient

from db.models import Base
from main import app
from dependencies import get_db


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
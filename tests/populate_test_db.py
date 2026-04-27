from db.models import CardapioTable
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv(".env.tests", override=True)

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_engine(TEST_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


# TUDO NO CARDÁPIO EM FORMATO .TITLE()
ITENS_TESTE = [
    
    {"nome": "Arroz", "categoria": "almoco", "preco": 10.0},
    {"nome": "Feijão", "categoria": "almoco", "preco": 8.0},
    {"nome": "Bife", "categoria": "almoco", "preco": 18.0},
    {"nome": "Frango", "categoria": "almoco", "preco": 16.0},
    {"nome": "Estrogonofe", "categoria": "almoco", "preco": 22.0},
    {"nome": "Purê", "categoria": "almoco", "preco": 12.0},

    {"nome": "Pizza Calabresa", "categoria": "Pizza", "preco": 35.0},
    {"nome": "Pizza Muçarela", "categoria": "Pizza", "preco": 30.0},
    {"nome": "Pizza Marguerita", "categoria": "Pizza", "preco": 32.0},

    {"nome": "Brownie", "categoria": "Sobremesas", "preco": 12.0},
    {"nome": "Pudim", "categoria": "Sobremesas", "preco": 10.0},
    {"nome": "Bolo de pote", "categoria": "Sobremesas", "preco": 15.0},

    {"nome": "Salada", "categoria": "legumes", "preco": 20.0},
    {"nome": "Vegana", "categoria": "legumes", "preco": 22.0},
    {"nome": "Vegetariana", "categoria": "legumes", "preco": 20.0},
]


def popular_db_teste():
    db = SessionLocal()

    try:
        for item in ITENS_TESTE:
            exists = db.query(CardapioTable).filter_by(nome=item["nome"]).first()

            if not exists:
                db.add(CardapioTable(**item))

        db.commit()

    finally:
        db.close()
# Arquivo para gerar o cardápio

from db.models import CardapioTable 

from db.database import SessionLocal


# TUDO NO CARDÁPIO EM FORMATO .TITLE()
ITENS_INICIAIS = [

    {
        "nome": "Escondidinho De Carne",
        "categoria": "almoco",
        "preco_tradicional": 25.0,
        "preco_pequeno": 20.0,
        "preco_grande": 35.0
    },

    {
        "nome": "Feijoada",
        "categoria": "almoco",
        "preco_tradicional": 27.0,
        "preco_pequeno": 22.0,
        "preco_grande": 38.0
    },

    {
        "nome": "Moqueca De Peixe",
        "categoria": "almoco",
        "preco_tradicional": 23.0,
        "preco_pequeno": 18.0,
        "preco_grande": 34.0
    },

    {
        "nome": "Frango Grelhado Com Legumes",
        "categoria": "almoco",
        "preco_tradicional": 26.0,
        "preco_pequeno": 21.0,
        "preco_grande": 37.0
    },

    {
        "nome": "Strogonoff De Frango",
        "categoria": "almoco",
        "preco_tradicional": 32.0,
        "preco_pequeno": 27.0,
        "preco_grande": 44.0
    },

    {
        "nome": "Parmegiana De Frango",
        "categoria": "almoco",
        "preco_tradicional": 29.0,
        "preco_pequeno": 24.0,
        "preco_grande": 41.0
    },

    {
        "nome": "Pizza Calabresa",
        "categoria": "Pizza",
        "preco_tradicional": 35.0,
        "preco_pequeno": 28.0,
        "preco_grande": 52.0
    },

    {
        "nome": "Pizza Muçarela",
        "categoria": "Pizza",
        "preco_tradicional": 30.0,
        "preco_pequeno": 24.0,
        "preco_grande": 47.0
    },

    {
        "nome": "Pizza Marguerita",
        "categoria": "Pizza",
        "preco_tradicional": 32.0,
        "preco_pequeno": 26.0,
        "preco_grande": 49.0
    },

    {
        "nome": "Brownie",
        "categoria": "Sobremesas",
        "preco_tradicional": 12.0,
        "preco_pequeno": 10.0,
        "preco_grande": 18.0
    },

    {
        "nome": "Pudim",
        "categoria": "Sobremesas",
        "preco_tradicional": 10.0,
        "preco_pequeno": 8.0,
        "preco_grande": 16.0
    },

    {
        "nome": "Bolo De Pote",
        "categoria": "Sobremesas",
        "preco_tradicional": 13.0,
        "preco_pequeno": 11.0,
        "preco_grande": 20.0
    },

    {
        "nome": "Salada",
        "categoria": "legumes",
        "preco_tradicional": 20.0,
        "preco_pequeno": 16.0,
        "preco_grande": 29.0
    },

    {
        "nome": "Vegana",
        "categoria": "legumes",
        "preco_tradicional": 22.0,
        "preco_pequeno": 18.0,
        "preco_grande": 31.0
    },

    {
        "nome": "Vegetariana",
        "categoria": "legumes",
        "preco_tradicional": 20.0,
        "preco_pequeno": 16.0,
        "preco_grande": 30.0
    },
]


def popular_cardapio():    
    db = SessionLocal()  
    try:
        for item in ITENS_INICIAIS:
            
            # verifica se o item já existe, pra não duplicar
            exists = db.query(CardapioTable).filter_by(
                nome=item["nome"]
                ).first()
            
            if not exists:
                novo_item = CardapioTable(
                    nome=item["nome"],
                    categoria=item["categoria"],
                    preco=item["preco"]
                )
                
                db.add(novo_item)   
                
        db.commit()
        print("Cardápio populado com sucesso!")
        
    except Exception as e:
        db.rollback()
        print("Erro ao popular cardápio:", e)
        
    finally:
        db.close()  
# Arquivo para gerar o cardápio

from db.models import CardapioTable 

from db.database import SessionLocal


# TUDO NO CARDÁPIO EM FORMATO .TITLE()
ITENS_INICIAIS = [
    
    {"nome": "Escondidinho De Carne", "categoria": "almoco", "preco": 25.0},
    {"nome": "Feijoada", "categoria": "almoco", "preco": 27.0},
    {"nome": "Moqueca De Peixe", "categoria": "almoco", "preco": 23.0},
    {"nome": "Frango Grelhado Com Legumes", "categoria": "almoco", "preco": 26.0},
    {"nome": "Strogonoff De Frango", "categoria": "almoco", "preco": 32.0},
    {"nome": "Parmegiana De Frango", "categoria": "almoco", "preco": 29.0},

    {"nome": "Pizza Calabresa", "categoria": "Pizza", "preco": 35.0},
    {"nome": "Pizza Muçarela", "categoria": "Pizza", "preco": 30.0},
    {"nome": "Pizza Marguerita", "categoria": "Pizza", "preco": 32.0},

    {"nome": "Brownie", "categoria": "Sobremesas", "preco": 12.0},
    {"nome": "Pudim", "categoria": "Sobremesas", "preco": 10.0},
    {"nome": "Bolo De Pote", "categoria": "Sobremesas", "preco": 13.0},

    {"nome": "Salada", "categoria": "legumes", "preco": 20.0},
    {"nome": "Vegana", "categoria": "legumes", "preco": 22.0},
    {"nome": "Vegetariana", "categoria": "legumes", "preco": 20.0},
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
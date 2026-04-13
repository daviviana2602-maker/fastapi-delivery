# Arquivo para gerar o cardápio

from models import CardapioTable, SessionLocal  


# TUDO NO CARDÁPIO EM FORMATO .TITLE()
ITENS_INICIAIS = [
    
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


# função que insere os ITENS_INICIAIS na tabela cardápio
def popular_cardapio():    
    db = SessionLocal()  # cria a sessão
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
                
                db.add(novo_item)   # adiciona o respectivo item na tabela cardápio
                
        db.commit()
        print("Cardápio populado com sucesso!")
        
    except Exception as e:
        db.rollback()
        print("Erro ao popular cardápio:", e)
        
    finally:
        db.close()  # fecha o banco
from sqlalchemy.orm import Session


#sessão pra mexer no banco de forma prática
def get_db():
    db = Session()    # abre a session
    try:
        yield db    # retorna a váriavel sem fechar a sessão
    finally:
        db.close()     # fecha a session
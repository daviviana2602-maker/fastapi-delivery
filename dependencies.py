# Função para sessões em rotas

from models import SessionLocal


#sessão pra mexer no banco de forma prática
def get_db():
    db = SessionLocal()    # abre a session
    try:
        yield db    # retorna a váriavel sem fechar a sessão
    finally:    
        db.close()     # fecha a session
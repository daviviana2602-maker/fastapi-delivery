# Função para sessões em rotas

from fastapi import Header

from token_utils import verificar_token

from models import SessionLocal



#sessão pra mexer no banco de forma prática
def get_db():
    db = SessionLocal()    # abre a session
    try:
        yield db    # retorna a váriavel sem fechar a sessão
    finally:    
        db.close()     # fecha a session
        
        
        
# Função para proteger rotas
def usuario_logado(authorization: str = Header(...)):   # (... = obrigatório) (front envia authorization já em JWT com Bearer)
    token = authorization.replace("Bearer ", "")    # remove o "Bearer ", sobrando só o JWT puro
    jwt_decodificado = verificar_token(token)    # chama verificar_token que valida e decodifica o token
    return jwt_decodificado.get("sub")  # retorna só o id
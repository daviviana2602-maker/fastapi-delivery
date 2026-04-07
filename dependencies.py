# Função para sessões em rotas

from sqlalchemy.orm import Session

from fastapi import Header, Depends

from token_utils import verificar_token

from models import SessionLocal



# sessão pra mexer no banco de forma prática
def get_db():
    db = SessionLocal()    # abre a session
    try:
        yield db    # retorna a váriavel sem fechar a sessão
    finally:    
        db.close()     # fecha a session
        
        
        
# Função para proteger rotas somente para usuários autenticados
def usuario_logado(
                authorization: str = Header(...),    # (... = obrigatório) (front envia authorization já em JWT com Bearer)
                db: Session = Depends(get_db)
                ):   
    token = authorization.replace("Bearer ", "")    # remove o "Bearer ", sobrando só o JWT puro
    jwt_decodificado = verificar_token(token, db)    # chama verificar_token que valida e decodifica o token e se o usuário existe no banco (com o db)
    return jwt_decodificado.get("sub")  # retorna só o id
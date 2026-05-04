from sqlalchemy.orm import Session

from fastapi import Header, Depends, HTTPException

from token_utils import verificar_token

from db.models import UserTable

from db.database import SessionLocal


def get_db():
    db = SessionLocal()    
    try:
        yield db    # retorna a váriavel sem fechar a sessão
    finally:    
        db.close()     
        
        
        
def usuario_logado(
                authorization: str = Header(...),    # (... = obrigatório) (front envia authorization já em JWT com Bearer)
                db: Session = Depends(get_db)
                ):   
    
    token = authorization.replace("Bearer ", "")    # remove o "Bearer ", sobrando só o JWT puro
    jwt_decodificado = verificar_token(token, db)    # chama verificar_token que valida e decodifica o token e se o usuário existe no banco (com o db)
    
    usuario_id = int(jwt_decodificado.get("sub"))
    
    usuario = db.query(UserTable).filter_by(    # checando quem é o usuário
        id=usuario_id
    ).first()
    
    if usuario.status == "DESATIVADO":
        raise HTTPException(status_code=403, detail="usuário desativado")
    
    if usuario.status == "EXCLUIDO":
        raise HTTPException(status_code=403, detail="usuário excluído")
    
    
    return usuario_id


def checar_admin(
    usuario_id: int = Depends(usuario_logado),
    db: Session = Depends(get_db)
):
     
    usuario = db.query(UserTable).filter_by(
        id=usuario_id
        ).first()
    
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")
    
    if not usuario.admin:
        raise HTTPException(status_code=403, detail="Você não tem permissão para essa ação")  
    
    return usuario  
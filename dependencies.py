# Função para sessões em rotas

from sqlalchemy.orm import Session

from fastapi import Header, Depends, HTTPException

from token_utils import verificar_token

from models import SessionLocal, UserTable



# sessão pra mexer no banco de forma prática
def get_db():
    db = SessionLocal()    # abre a session
    try:
        yield db    # retorna a váriavel sem fechar a sessão
    finally:    
        db.close()     # fecha a session
        
        
        
# Função para proteger rotas somente para usuários autenticados e ativados
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
    
    if not usuario.ativo:
        raise HTTPException(status_code=403, detail="usuário desativado")
    
    return usuario_id



def checar_dono_ou_admin(
    recurso_usuario_id: int,          # id do dono do recurso
    usuario_id: int = Depends(usuario_logado),
    db: Session = Depends(get_db)
):

    usuario = db.query(UserTable).filter_by(
        id=usuario_id
        ).first()
    
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    if recurso_usuario_id != usuario_id and not usuario.admin:
        raise HTTPException(status_code=403, detail="Você não tem permissão para realizar essa ação")   # se não for o dono do recurso ou o admin

    return True     # se passou na verificação, libera o acesso



def checar_admin(
    usuario_id: int = Depends(usuario_logado),
    db: Session = Depends(get_db)
):
     
    usuario = db.query(UserTable).filter_by(
        id=usuario_id
        ).first()
    
    if not usuario or not usuario.admin:
        raise HTTPException(status_code=403, detail="Você não tem permissão para essa ação") # não é administrador
    
    return usuario  # retorna o objeto do usuário logado se for admin (linha inteira do banco referente ao id em questão)
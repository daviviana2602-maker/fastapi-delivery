# Função para checar se um usuário é dono de tal recurso ou se é admin

from fastapi import HTTPException, Depends

from sqlalchemy.orm import Session

from dependencies import get_db, usuario_logado

from models import UserTable


# Não é uma dependência, porque depende de recurso_usuario_id, que muda dependendo da utilização
def checar_dono_ou_admin(
    recurso_usuario_id: int,  # id do dono do recurso (pedido, item, etc)
    usuario_id: int = Depends(usuario_logado),
    db: Session = Depends(get_db)
):
    
    usuario = db.query(UserTable).filter_by(
        id=usuario_id
        ).first()
    
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    if recurso_usuario_id != usuario_id and not usuario.admin:
        raise HTTPException(status_code=403, detail="Você não tem permissão")   # se não for o dono do recurso e nem adm

    return True
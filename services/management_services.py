from sqlalchemy.orm import Session

from fastapi import HTTPException

from db.models import UserTable

from schemas import AlterationUserSchema

from helpers import resposta_sucesso



def promover_usuario_services(
        promote_user: AlterationUserSchema,
        db: Session,
        admin: UserTable    
        ):
    
    
    usuario_a_promover = db.query(UserTable).filter_by(
        id=promote_user.usuario_a_sofrer_alteracao
        ).first()

    
    if not usuario_a_promover:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")   
    
    if usuario_a_promover.status == "DESATIVADO":
        raise HTTPException(status_code=400, detail="usuário está desativado e não pode ser promovido")
    
    if usuario_a_promover.status == "EXCLUIDO":
        raise HTTPException(status_code=400, detail="usuário foi excluído e não pode sofrer alterações")
    
    if usuario_a_promover.admin == True:
        raise HTTPException(status_code=403, detail="O usuário escolhido já é um administrador")
    
    usuario_a_promover.admin = True
    
    try:
        db.commit()
        db.refresh(usuario_a_promover)
    except Exception:
        db.rollback()
        raise
    
    
    return resposta_sucesso(            
        f"Usuário {usuario_a_promover.nome} agora é admin",    
        {
            "id": usuario_a_promover.id,
        }
    )
        
        
        
def rebaixar_usuario_services(
        demote_user: AlterationUserSchema,
        db: Session,
        admin: UserTable    
        ):
    
    
    usuario_a_rebaixar = db.query(UserTable).filter_by(
        id=demote_user.usuario_a_sofrer_alteracao
        ).first()
    
    
    if not usuario_a_rebaixar:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")   
    
    if usuario_a_rebaixar.id == 1:
        raise HTTPException(status_code=404, detail="Usuário não pode ser rebaixado")   # proteção para o "super admin"
    
    if usuario_a_rebaixar.admin == False:
        raise HTTPException(status_code=403, detail="O usuário escolhido não é administrador")
    
    if usuario_a_rebaixar.status == "EXCLUIDO":
        raise HTTPException(status_code=400, detail="usuário foi excluído e não pode sofrer alterações")
    
    if usuario_a_rebaixar.id == admin.id:
        raise HTTPException(status_code=403, detail="Você não pode se rebaixar")    
    
    
    usuario_a_rebaixar.admin = False
    
    try:
        db.commit()
        db.refresh(usuario_a_rebaixar)
    except Exception:
        db.rollback()
        raise
    
    
    return resposta_sucesso(           
        f"Usuário {usuario_a_rebaixar.nome} agora não é mais admin",    
        {
            "id": usuario_a_rebaixar.id,
        }
    )
   
    
    
def desativar_usuario_services(
    delete_user_id: AlterationUserSchema,
    db: Session,
    admin: UserTable    
):
    

    usuario = db.query(UserTable).filter_by(
        id=delete_user_id.usuario_a_sofrer_alteracao
    ).first()
    
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if usuario.admin:
        raise HTTPException(status_code=403, detail="O usuário escolhido é administrador e não pode ser desativado")
    
    if usuario.status == "DESATIVADO":
        raise HTTPException(status_code=400, detail="Usuário já está desativado")  
    
    if usuario.status == "EXCLUIDO":
        raise HTTPException(status_code=400, detail="usuário foi excluído e não pode sofrer alterações")
    
    
    usuario.status = "DESATIVADO"   
    
    try:
        db.commit()
        db.refresh(usuario)
    except Exception:
        db.rollback()
        raise
    
    
    return resposta_sucesso(            
        f"Usuário {usuario.nome} foi desativado",    
        {
            "id": usuario.id,
        }
    )
   
    
    
def reativar_usuario_services(
    reactive_user_id: AlterationUserSchema,
    db: Session,
    admin: UserTable    
):
    
  
    usuario = db.query(UserTable).filter_by(
        id=reactive_user_id.usuario_a_sofrer_alteracao
        ).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if usuario.status == "ATIVO":
        raise HTTPException(status_code=400, detail="Usuário já está ativo")
    
    if usuario.status == "EXCLUIDO":
        raise HTTPException(status_code=400, detail="usuário foi excluído e não pode sofrer alterações")
    
    usuario.status = "ATIVO"
    
    try:
        db.commit()
        db.refresh(usuario)
    except Exception:
        db.rollback()
        raise
    
    
    return resposta_sucesso(            
        f"Usuário {usuario.nome} foi reativado",    
        {
            "id": usuario.id,
        }
    )
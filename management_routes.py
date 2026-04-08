# Rotas para administração do app

from sqlalchemy.orm import Session

from dependencies import get_db, usuario_logado, checar_admin

from fastapi import APIRouter, Depends, HTTPException

from models import UserTable

from schemas import PromoteUserSchema, DemoteUserSchema, DeleteUserSchema


management_router = APIRouter(prefix = "/management", tags=["management"])   # define o caminho = domínio/management/(rota esolhinha)



@management_router.post("/promover_usuario")
async def promover_usuario(
                    promote_user_schema: PromoteUserSchema,
                    db: Session = Depends(get_db),
                    admin: UserTable = Depends(checar_admin)    # checando se é admin e quem é pelo id
                    ):
    
    # Procura o usuário a ser promovido
    usuario_a_promover = db.query(UserTable).filter_by(
        id=promote_user_schema.usuario_a_promover_id
        ).first()
    
    if not usuario_a_promover:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")   # usuário inexistente retorna erro
    
    if usuario_a_promover.admin == True:
        raise HTTPException(status_code=403, detail="O usuário escolhido já é um administrador")
    
    usuario_a_promover.admin = True
    db.commit()
    db.refresh(usuario_a_promover)
    
    return {
            "msg": f"Usuário {usuario_a_promover.nome} agora é admin",
            "usuario_id": usuario_a_promover.id
            }
        
        
        
@management_router.post("/rebaixar_usuario")
async def rebaixar_usuario(
                    demote_user_schema: DemoteUserSchema,
                    db: Session = Depends(get_db),
                    admin: UserTable = Depends(checar_admin)    # checando se é admin e quem é pelo id
                    ):
    
    # Procura o usuário a ser rebaixado
    usuario_a_rebaixar = db.query(UserTable).filter_by(
        id=demote_user_schema.usuario_a_rebaixar_id
        ).first()
    
    if not usuario_a_rebaixar:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")   # usuário inexistente retorna erro
    
    if usuario_a_rebaixar.admin == False:
        raise HTTPException(status_code=403, detail="O usuário escolhido não é administrador")
    
    if usuario_a_rebaixar.id == admin.id:
        raise HTTPException(status_code=403, detail="Você não pode se rebaixar")    # checagem pra não deixar se rebaixar sozinho
    
    usuario_a_rebaixar.admin = False
    db.commit()
    db.refresh(usuario_a_rebaixar)
    
    return {
            "msg": f"Usuário {usuario_a_rebaixar.nome} agora não é mais admin",
            "usuario_id": usuario_a_rebaixar.id
            }    
    
    
    
@management_router.delete("/deletar_usuario")
async def deletar_usuario(
                    delete_user_schema: DeleteUserSchema,
                    db: Session = Depends(get_db),
                    admin: UserTable = Depends(checar_admin)    # checando se é admin e quem é pelo id
                    ):
    
    # Procura o usuário a ser deletado
    usuario_a_deletar = db.query(UserTable).filter_by(
        id=delete_user_schema.usuario_a_deletar_id
        ).first()
    
    if not usuario_a_deletar:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")   # usuário inexistente retorna erro
    
    if usuario_a_deletar.admin == True:
        raise HTTPException(status_code=403, detail="O usuário escolhido é administrador e não pode ser deletado")  # não deixa se deletar e nem deletar outro adm
    
    
    db.delete(usuario_a_deletar)    # deletando usuario
    db.commit()
    
    return {
            "msg": f"Usuário {usuario_a_deletar.nome} foi deletado",
            "usuario_id":usuario_a_deletar.id
            }    
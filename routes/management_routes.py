# Rotas para administração do app

from sqlalchemy.orm import Session

from dependencies import get_db, checar_admin

from fastapi import APIRouter, Depends, HTTPException

from models import UserTable

from schemas import AlterationUserSchema

from response_schemas import CommonResponse

from helpers import resposta_sucesso



management_router = APIRouter(prefix = "/management", tags=["management"])   # define o caminho = domínio/management/(rota esolhinha)



@management_router.patch("/promover_usuario", response_model=CommonResponse)
async def promover_usuario(
                    promote_user: AlterationUserSchema,
                    db: Session = Depends(get_db),
                    admin: UserTable = Depends(checar_admin)    # checando se é admin e quem é pelo id
                    ):
    
    
    # Procura o usuário a ser promovido
    usuario_a_promover = db.query(UserTable).filter_by(
        id=promote_user.usuario_a_sofrer_alteracao
        ).first()
    
    
    if not usuario_a_promover.ativo:
        raise HTTPException(status_code=400, detail="usuário está desativado e não pode ser promovido")
    
    if not usuario_a_promover:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")   # usuário inexistente retorna erro
    
    if usuario_a_promover.admin == True:
        raise HTTPException(status_code=403, detail="O usuário escolhido já é um administrador")
    
    usuario_a_promover.admin = True
    db.commit()
    db.refresh(usuario_a_promover)
    
    
    return resposta_sucesso(            # success já vem como True pela função
        f"Usuário {usuario_a_promover.nome} agora é admin",    
        {
            "id": usuario_a_promover.id,
        }
    )
        
        
        
@management_router.patch("/rebaixar_usuario", response_model=CommonResponse)
async def rebaixar_usuario(
                    demote_user: AlterationUserSchema,
                    db: Session = Depends(get_db),
                    admin: UserTable = Depends(checar_admin)    # checando se é admin e quem é pelo id
                    ):
    
    
    # Procura o usuário a ser rebaixado
    usuario_a_rebaixar = db.query(UserTable).filter_by(
        id=demote_user.usuario_a_sofrer_alteracao
        ).first()
    
    
    if not usuario_a_rebaixar:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")   
    
    if usuario_a_rebaixar.admin == False:
        raise HTTPException(status_code=403, detail="O usuário escolhido não é administrador")
    
    if usuario_a_rebaixar.id == admin.id:
        raise HTTPException(status_code=403, detail="Você não pode se rebaixar")    # checagem pra não deixar se rebaixar sozinho
    
    
    usuario_a_rebaixar.admin = False
    db.commit()
    db.refresh(usuario_a_rebaixar)
    
    
    return resposta_sucesso(            # success já vem como True pela função
        f"Usuário {usuario_a_rebaixar.nome} agora não é mais admin",    
        {
            "id": usuario_a_rebaixar.id,
        }
    )
   
    
    
@management_router.patch("/desativar_usuario", response_model=CommonResponse)
async def desativar_usuario(
    delete_user_id: AlterationUserSchema,
    db: Session = Depends(get_db),
    admin: UserTable = Depends(checar_admin)    # checando se é admin e quem é pelo id
):
    
    # Procura o usuário a ser desativado
    usuario = db.query(UserTable).filter_by(
        id=delete_user_id.usuario_a_sofrer_alteracao
    ).first()
    
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if usuario.admin:
        raise HTTPException(status_code=403, detail="O usuário escolhido é administrador e não pode ser desativado")
    
    if not usuario.ativo:
        raise HTTPException(status_code=400, detail="Usuário já está desativado")   # contas "banidas"/desativadas
    
    
    usuario.ativo = False   # desativando usuário
    
    db.commit()
    db.refresh(usuario)
    
    
    return resposta_sucesso(            # success já vem como True pela função
        f"Usuário {usuario.nome} foi desativado",    
        {
            "id": usuario.id,
        }
    )
   
    
    
@management_router.patch("/reativar_usuario", response_model=CommonResponse)
async def reativar_usuario(
    reactive_user_id: AlterationUserSchema,
    db: Session = Depends(get_db),
    admin: UserTable = Depends(checar_admin)    # checando se é admin e quem é pelo id
):
    
    # Procura o usuário a ser reativado
    usuario = db.query(UserTable).filter_by(
        id=reactive_user_id.usuario_a_sofrer_alteracao
        ).first()
    
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    
    if usuario.ativo:
        raise HTTPException(status_code=400, detail="Usuário já está ativo")
    
    usuario.ativo = True    # reativando o usuário
    
    db.commit()
    db.refresh(usuario)
    
    
    return resposta_sucesso(            # success já vem como True pela função
        f"Usuário {usuario.nome} foi reativado",    
        {
            "id": usuario.id,
        }
    )
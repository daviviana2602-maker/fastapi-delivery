from services.profile_services import editar_perfil_services, excluir_usuario_services

from sqlalchemy.orm import Session

from dependencies import get_db, usuario_logado

from schemas import UpdateProfileSchema

from response_schemas import CommonResponse

from fastapi import APIRouter, Depends


profile_router = APIRouter(prefix = "/profile", tags=["profile"]) 



@profile_router.patch("/editar_perfil", response_model=CommonResponse)
def editar_perfil(
        update_user: UpdateProfileSchema,
        usuario_id: int = Depends(usuario_logado),
        db: Session = Depends(get_db)
        ):
    
    return editar_perfil_services(update_user, usuario_id, db)
    
    
   
@profile_router.delete("/excluir_conta", response_model=CommonResponse)
def excluir_usuario(
        senha_atual: str,
        db: Session = Depends(get_db),
        usuario_id: int = Depends(usuario_logado)
        ):

    return excluir_usuario_services(senha_atual, db, usuario_id)
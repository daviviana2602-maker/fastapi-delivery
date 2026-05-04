from services.management_services import promover_usuario_services, rebaixar_usuario_services, reativar_usuario_services, desativar_usuario_services

from sqlalchemy.orm import Session

from dependencies import get_db, checar_admin

from fastapi import APIRouter, Depends

from db.models import UserTable

from schemas import AlterationUserSchema

from response_schemas import CommonResponse


management_router = APIRouter(prefix = "/management", tags=["management"])   



@management_router.patch("/promover_usuario", response_model=CommonResponse)
def promover_usuario(
        promote_user: AlterationUserSchema,
        db: Session = Depends(get_db),
        admin: UserTable = Depends(checar_admin)    
        ):
    
    return promover_usuario_services(promote_user, db, admin)
        
        
        
@management_router.patch("/rebaixar_usuario", response_model=CommonResponse)
def rebaixar_usuario(
                    demote_user: AlterationUserSchema,
                    db: Session = Depends(get_db),
                    admin: UserTable = Depends(checar_admin)   
                    ):
    
    return rebaixar_usuario_services(demote_user, db, admin)
   
    
    
@management_router.patch("/desativar_usuario", response_model=CommonResponse)
def desativar_usuario(
        delete_user_id: AlterationUserSchema,
        db: Session = Depends(get_db),
        admin: UserTable = Depends(checar_admin)    
        ):
    
    return desativar_usuario_services(delete_user_id, db, admin)
   
    
    
@management_router.patch("/reativar_usuario", response_model=CommonResponse)
def reativar_usuario(
    reactive_user_id: AlterationUserSchema,
    db: Session = Depends(get_db),
    admin: UserTable = Depends(checar_admin)   
    ):
    
    return reativar_usuario_services(reactive_user_id, db, admin)
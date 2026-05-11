from services.auth_services import criar_conta_services, login_services, use_refresh_token_services, me_service, esqueci_senha_service, redefinir_senha_service

from sqlalchemy.orm import Session

from dependencies import get_db, usuario_logado

from schemas import CreateUserSchema, LoginSchema, TokenSchema, EsqueciSenhaSchema, RedefinirSenhaSchema

from response_schemas import CommonResponse

from fastapi import APIRouter, Depends


auth_router = APIRouter(prefix = "/auth", tags=["auth"])   
    


@auth_router.post("/criar_conta", response_model=CommonResponse)
def criar_conta(
            create_user: CreateUserSchema,
            db: Session = Depends(get_db)
            ):

    return criar_conta_services(create_user, db)



@auth_router.post("/login", response_model=CommonResponse) 
def login(
        user_login: LoginSchema,
        db: Session = Depends(get_db)
        ):

    return login_services(user_login, db)
    
    
    
@auth_router.post("/refresh", response_model=CommonResponse)   # usa refresh token para gerar um novo access token sem exigir login novamente
def use_refresh_token(
        receive_refresh_token: TokenSchema,
        db: Session = Depends(get_db)
        ):     
    
    return use_refresh_token_services(receive_refresh_token, db)



@auth_router.get("/me")
def me(
    usuario_id: int = Depends(usuario_logado),
    db: Session = Depends(get_db)
    ):
    
    return me_service(usuario_id, db)



@auth_router.post("/esqueci_a_senha")
def recuperar_conta(
    receive_email: EsqueciSenhaSchema,
    db: Session = Depends(get_db)
):

    return esqueci_senha_service(receive_email, db)



@auth_router.post("/redefinir_senha")
def redefinir_senha(
    redefinir: RedefinirSenhaSchema,
    db: Session = Depends(get_db)
):

    return redefinir_senha_service(redefinir, db)
# Rotas para Autenticação

from sqlalchemy.orm import Session

from dependencies import get_db

from models import UserTable

from schemas import UserSchema, LoginSchema, TokenSchema

from security import argon_context

from token_utils import criar_token, verificar_token

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException


auth_router = APIRouter(prefix = "/auth", tags=["auth"])   # define o caminho = domínio/auth/(rota esolhinha)



@auth_router.get("/")   # rota de entrada (inicial)
async def home():
    
    return {"msg": "você acessou a tela de autenticação"}
    

@auth_router.post("/criar_conta")
async def criar_conta(
                    user_schema: UserSchema,
                    db: Session = Depends(get_db)
                    ):
    
    # checa se usuário já existe
    usuario = db.query(UserTable).filter_by(
    email=user_schema.email
    ).first()
    
    if usuario:
        raise HTTPException(status_code = 400, detail = "já existe um usuário com esse email")     
    
    
    senha_criptografada = argon_context.hash(user_schema.senha)    # criptografando senha
    
    novo_usuario = UserTable(
        nome = user_schema.nome,
        email = user_schema.email,
        senha = senha_criptografada,
        ativo = user_schema.ativo,
        admin = user_schema.admin
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)    # garante que campos gerados pelo banco (como id) estejam disponíveis (atualiza)

    return {"msg": f"usuário {user_schema.nome} criado com sucesso!", "id": novo_usuario.id} 


@auth_router.post("/login") 
async def login(
                login_schema: LoginSchema,
                db: Session = Depends(get_db)
                ):

    # checa se usuário existe
    usuario = db.query(UserTable).filter_by(
    email=login_schema.email
    ).first()
    
    if not usuario:
        raise HTTPException(status_code = 400, detail = "email ou senha inválidos")    
    
    if not argon_context.verify(login_schema.senha, usuario.senha):     # verifica se a senha está correta, mesmo estando criptografada
        raise HTTPException(status_code=400, detail="email ou senha inválidos")     


    access_token = criar_token(usuario.id)      # criando token (com tempo pré determinado de duração na função) para o usuário que acabou de logar (ID)
    refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))     # criando outro token com maior duração
    
    return{
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
           }
    
    
@auth_router.post("/refresh")   # usa refresh token para gerar um novo access token sem exigir login novamente
async def use_refresh_token(token_schema: TokenSchema):     # cliente manda refresh_token (front end decide quando usar essa rota)
    
    jwt_decodificado = verificar_token(token_schema.refresh_token)    # Decodificando JWT

    usuario_id = jwt_decodificado.get("sub")    # descobrindo a quem pertence o token (decodificando o JWT e pegando usuario_id no "sub")

    access_token = criar_token(usuario_id)  # criando novo access_token com base no JWT decodificado colocado no usuario_id

    return {
        "access_token": access_token,
        "token_type": "Bearer"
    }
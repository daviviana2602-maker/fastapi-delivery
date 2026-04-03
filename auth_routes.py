# Autenticação
from sqlalchemy.orm import Session

from dependencies import get_db

from models import UserTable

from schemas import UserSchema, LoginSchema

from security import argon_context

from fastapi import APIRouter, Depends, HTTPException


auth_router = APIRouter(prefix = "/auth", tags=["auth"])   # define o caminho = domínio/auth/(rota esolhinha)



# Função para criação de tokens
def criar_token(usuario_id):
    token = f"akgywsndfirf{usuario_id}" 
    return token
    


@auth_router.get("/")   # rota de entrada (inicial)
async def home():
    
    return {"msg": "você acessou a tela de autenticação"}
    

@auth_router.post("/criar_conta")   # rota para criação de conta
async def criar_conta(
                    UserSchema: UserSchema,
                    db: Session = Depends(get_db)
                    ):
    
    # checa se usuário já existe
    usuario = db.query(UserTable).filter_by(
    email=UserSchema.email
    ).first()
    
    if usuario:
        raise HTTPException(status_code = 400, detail = "já existe um usuário com esse email")     # Retornando código do erro e mensagem
    
    
    senha_criptografada = argon_context.hash(UserSchema.senha)    # criptografando senha
    
    novo_usuario = UserTable(
        nome = UserSchema.nome,
        email = UserSchema.email,
        senha = senha_criptografada,
        ativo = UserSchema.ativo,
        admin = UserSchema.admin
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)    # garante que campos gerados pelo banco (como id) estejam disponíveis (atualiza)

    return {"msg": f"usuário {UserSchema.nome} criado com sucesso!", "id": novo_usuario.id}     # Retornando mensagem de sucesso


@auth_router.post("/login")
async def login(
                LoginSchema: LoginSchema,
                db: Session = Depends(get_db)
                ):

    # checa se usuário existe
    usuario = db.query(UserTable).filter_by(
    email=LoginSchema.email
    ).first()
    
    if not usuario:
        raise HTTPException(status_code = 400, detail = "email ou senha inválidos")     # Retornando código do erro e mensagem
    
    if not argon_context.verify(LoginSchema.senha, usuario.senha):  # verifica se a senha está correta, mesmo estando criptografada
        raise HTTPException(status_code=400, detail="email ou senha inválidos")     # Retornando código do erro e mensagem


    access_token = criar_token(usuario.id)  # pega o ID do usuário que acabou de logar e coloca dentro do token
    
    return{
            "access_token": access_token,
            "token_type": "Bearer"
           }
# Autenticação
from pydantic import EmailStr

from sqlalchemy.orm import Session

from dotenv import load_dotenv
import os
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

from dependencies import get_db

from models import UserTable

from security import bcrypt_context

from fastapi import APIRouter, Depends


auth_router = APIRouter(prefix = "/auth", tags=["auth"])   # define o caminho = domínio/auth/(rota esolhinha)


@auth_router.get("/")
async def home():
    
    return {"msg": "você acessou a tela de autenticação"}
    

@auth_router.post("/criar_conta")
async def criar_conta(
                    email: EmailStr,
                    senha: str,
                    nome: str,
                    db: Session = Depends(get_db)
                    ):
    
    # checa se usuário já existe
    usuario = db.query(UserTable).filter_by(
    email=email
    ).first()
    
    if usuario:
        return {"erro": "já existe um usuário com esse email"}
    
    senha_criptografada = bcrypt_context.hash(senha)    # criptografando senha
    novo_usuario = UserTable(
        email=email,
        senha=senha_criptografada, 
        nome=nome
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return {"msg": "usuário criado", "id": novo_usuario.id}
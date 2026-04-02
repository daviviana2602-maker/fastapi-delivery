# Autenticação
from pydantic import EmailStr

from sqlalchemy.orm import Session

from dependencies import get_db

from models import UserTable

from fastapi import APIRouter, Depends


auth_router = APIRouter(prefix = "/auth", tags=["auth"])   # define o caminho = domínio/auth/(rota esolhinha)


@auth_router.get("/")
async def home():
    
    return {"msg": "você acessou a tela de autenticação"}
    

@auth_router.post("/criar_conta")
async def criar_conta(
                    email: EmailStr,
                    senha: str,
                    db: Session = Depends(get_db)
                    ):
    
    # checa se usuário já existe
    usuario = db.query(UserTable).filter_by(
    email=email
    ).first()
    
    if usuario:
        return{"já existe um usuário com esse email"}
    
    
    novo_usuario = UserTable(
        email=email,
        senha=senha,   # futuramente usar hash
        nome="default"
    )

    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)

    return {"msg": "usuário criado", "id": novo_usuario.id}
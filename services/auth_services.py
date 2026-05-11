from sqlalchemy.orm import Session

from db.models import UserTable

from schemas import CreateUserSchema, LoginSchema, TokenSchema, EsqueciSenhaSchema, RedefinirSenhaSchema

from helpers import resposta_sucesso, reset_email

from security import argon_context

from token_utils import criar_token, verificar_token

from datetime import timedelta, datetime

from fastapi import HTTPException

import secrets



def criar_conta_services(
        create_user: CreateUserSchema,
        db: Session
        ):
    
    usuario = db.query(UserTable).filter_by(
    email=create_user.email
    ).first()
    
    if usuario:
        raise HTTPException(status_code = 400, detail = "já existe um usuário com esse email")     
    
    
    senha_criptografada = argon_context.hash(create_user.senha)    # criptografando senha
    
    novo_usuario = UserTable(
        nome = create_user.nome,
        email = create_user.email,
        senha = senha_criptografada,
    )  
    
    
    try:
        db.add(novo_usuario)
        db.flush()   # enviando alterações pendentes para o banco dentro da transação aberta (um commit só durante a transação)

        if novo_usuario.id == 1:
            novo_usuario.admin = True

        db.commit()
        db.refresh(novo_usuario)
    except Exception:
        db.rollback()
        raise
        
    
    if novo_usuario.admin:
        return resposta_sucesso(           
        f"usuário {create_user.nome} criado com sucesso como admin!",   
        {
            "id": novo_usuario.id,
        }
        )
    

    return resposta_sucesso(            
        f"usuário {create_user.nome} criado com sucesso!",   
        {
            "id": novo_usuario.id,
        }
    )



def login_services(
        user_login: LoginSchema,
        db: Session
        ):


    usuario = db.query(UserTable).filter_by(
    email=user_login.email
    ).first()
    
    if not usuario:
        raise HTTPException(status_code = 400, detail = "email ou senha inválidos")   
    
    if usuario.status == "DESATIVADO":
        raise HTTPException(status_code=403, detail="usuário desativado") 
    
    if usuario.status == "EXCLUIDO":
        raise HTTPException(status_code=403, detail="usuário excluído") 
    
    if not argon_context.verify(user_login.senha, usuario.senha):     # verifica se a senha está correta, mesmo estando criptografada por comparação de hash
        raise HTTPException(status_code=400, detail="email ou senha inválidos")     


    access_token = criar_token(usuario.id)      
    refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))     
    
    
    return resposta_sucesso(            
        f"usuário logado com sucesso!",   
        {
            "id": usuario.id,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }
    )
    
    
    
def use_refresh_token_services(
        receive_refresh_token: TokenSchema,   
        db: Session
        ):     
    
    jwt_decodificado = verificar_token(receive_refresh_token.refresh_token, db)    

    usuario_id = jwt_decodificado.get("sub")    # descobrindo a quem pertence o token (decodificando o JWT e pegando usuario_id no "sub")

    access_token = criar_token(usuario_id)  


    return resposta_sucesso(            
        f"novo access token gerado com sucesso!",   
        {
            "access_token": access_token,
            "token_type": "Bearer"
        }
    )
    
    

def me_service(usuario_id: int, db: Session):

    usuario = db.query(UserTable).filter(
        UserTable.id == usuario_id
        ).first()

    return resposta_sucesso(            
        f"usuário carregado com sucesso!",
        {
        "id": usuario.id,
        "email": usuario.email,
        "admin": usuario.admin
        }
    )


def esqueci_senha_service(
    receive_email: EsqueciSenhaSchema,
    db: Session
    ):
    
    usuario = db.query(UserTable).filter_by(
        email=receive_email.email
    ).first()

    if not usuario:
        raise HTTPException(status_code=404, detail="usuário não encontrado")


    token = secrets.token_urlsafe(32)

    usuario.reset_token = token

    usuario.reset_token_expira_em = datetime.utcnow() + timedelta(minutes=10)

    db.commit()


    reset_email(
        to_email=receive_email.email,
        token=token
    )


    return resposta_sucesso(
        "email enviado com sucesso!",
        {
            "email": receive_email.email
        }
    )
    
    

def redefinir_senha_service(
    redefinir: RedefinirSenhaSchema,
    db: Session
):

    usuario = db.query(UserTable).filter_by(
        reset_token=redefinir.token
    ).first()


    if not usuario:
        raise HTTPException(status_code=400, detail="token inválido")


    if datetime.utcnow() > usuario.reset_token_expira_em:
        raise HTTPException(status_code=400, detail="token expirado")


    nova_senha_criptografada = argon_context.hash(redefinir.nova_senha)

    usuario.senha = nova_senha_criptografada

    usuario.reset_token = None
    
    usuario.reset_token_expira_em = None

    db.commit()


    return resposta_sucesso(
        "senha redefinida com sucesso!",
        {
        "id": usuario.id,
        "email": usuario.email
        }
    )
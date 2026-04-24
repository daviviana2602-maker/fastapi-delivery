# Services para as rotas para Autenticação

from sqlalchemy.orm import Session

from models import UserTable

from schemas import CreateUserSchema, LoginSchema, TokenSchema

from helpers import resposta_sucesso

from security import argon_context

from token_utils import criar_token, verificar_token

from datetime import timedelta

from fastapi import HTTPException



def criar_conta_services(
        create_user: CreateUserSchema,
        db: Session
        ):
    
    
    # checa se usuário já existe
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
    )   # colunas ativo e admin já são definidos por padrão default na UserTable no models 
    
    
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
        return resposta_sucesso(            # success já vem como True pela função
        f"usuário {create_user.nome} criado com sucesso como admin!",   
        {
            "id": novo_usuario.id,
        }
        )
    

    return resposta_sucesso(            # success já vem como True pela função
        f"usuário {create_user.nome} criado com sucesso!",   
        {
            "id": novo_usuario.id,
        }
    )



def login_services(
        user_login: LoginSchema,
        db: Session
        ):


    # checa se usuário existe
    usuario = db.query(UserTable).filter_by(
    email=user_login.email
    ).first()
    
    if not usuario:
        raise HTTPException(status_code = 400, detail = "email ou senha inválidos")   
    
    if not usuario.ativo:
        raise HTTPException(status_code=403, detail="usuário desativado") 
    
    if not argon_context.verify(user_login.senha, usuario.senha):     # verifica se a senha está correta, mesmo estando criptografada por comparação de hash
        raise HTTPException(status_code=400, detail="email ou senha inválidos")     


    access_token = criar_token(usuario.id)      # criando token (com tempo pré determinado de duração na função) para o usuário que acabou de logar (ID)
    refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))     # criando outro token com maior duração
    
    
    return resposta_sucesso(            # success já vem como True pela função
        f"usuário logado com sucesso!",   
        {
            "id": usuario.id,
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }
    )
    
    
    
def use_refresh_token_services(
        receive_refresh_token: TokenSchema,   # cliente manda refresh_token (front end decide quando usar essa rota)
        db: Session
        ):     
    
    jwt_decodificado = verificar_token(receive_refresh_token.refresh_token, db)    # analisando JWT

    usuario_id = jwt_decodificado.get("sub")    # descobrindo a quem pertence o token (decodificando o JWT e pegando usuario_id no "sub")

    access_token = criar_token(usuario_id)  # criando novo access_token com base no JWT decodificado colocado no usuario_id


    return resposta_sucesso(            # success já vem como True pela função
        f"novo access token gerado com sucesso!",   
        {
            "access_token": access_token,
            "token_type": "Bearer"
        }
    )
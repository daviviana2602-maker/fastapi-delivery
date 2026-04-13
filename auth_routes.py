# Rotas para Autenticação

from sqlalchemy.orm import Session

from dependencies import get_db

from models import UserTable

from schemas import CreateUserSchema, LoginSchema, TokenSchema

from response_schemas import CommonResponse

from helpers import resposta_sucesso

from security import argon_context

from token_utils import criar_token, verificar_token

from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException



auth_router = APIRouter(prefix = "/auth", tags=["auth"])   # define o caminho = domínio/auth/(rota escolhida)
    


@auth_router.post("/criar_conta", response_model=CommonResponse)
async def criar_conta(
                    create_user: CreateUserSchema,
                    db: Session = Depends(get_db)
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
    
    db.add(novo_usuario)
    db.commit()
    db.refresh(novo_usuario)    # garante que campos gerados pelo banco (como id) estejam disponíveis (atualiza)
    
    
    # o primeiro usuário sempre se torna admin
    if novo_usuario.id == 1:
        novo_usuario.admin = True   
        db.commit()
        db.refresh(novo_usuario)
        
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



@auth_router.post("/login", response_model=CommonResponse) 
async def login(
                user_login: LoginSchema,
                db: Session = Depends(get_db)
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
    
    
    
@auth_router.post("/refresh")   # usa refresh token para gerar um novo access token sem exigir login novamente
async def use_refresh_token(
                        receive_refresh_token: TokenSchema,   # cliente manda refresh_token (front end decide quando usar essa rota)
                        db: Session = Depends(get_db)
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
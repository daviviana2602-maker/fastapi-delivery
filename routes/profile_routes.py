# Rotas para Perfil

from sqlalchemy.orm import Session

from dependencies import get_db, usuario_logado

from models import UserTable, ExcludedUserTable

from schemas import UpdateProfileSchema

from response_schemas import CommonResponse

from helpers import resposta_sucesso, checar_dono_ou_admin

from security import argon_context

from fastapi import APIRouter, Depends, HTTPException


profile_router = APIRouter(prefix = "/profile", tags=["profile"])   # define o caminho = domínio/profile/(rota escolhida)


@profile_router.patch("/editar_perfil", response_model=CommonResponse)
async def editar_perfil(
                    update_user: UpdateProfileSchema,
                    usuario_id: int = Depends(usuario_logado),
                    db: Session = Depends(get_db)
                    ):
    
    # pegando id do usuário
    usuario = db.query(UserTable).filter_by(
        id=usuario_id
        ).first()


    if not usuario:
        raise HTTPException(status_code = 404, detail = "usuário não encontrado")


    # pede senha para dados de segurança
    if update_user.email or update_user.senha:
        if not update_user.senha_atual:
            raise HTTPException(status_code = 400, detail = "senha atual é obrigatória para mudanças de email e senha")


        if not argon_context.verify(update_user.senha_atual, usuario.senha):    # verifica se a senha está correta, mesmo estando criptografada por comparação de hash
            raise HTTPException(status_code = 400, detail = "senha atual inválida")


    # mudança de nome
    if update_user.nome:
        usuario.nome = update_user.nome


    # mudança email
    if update_user.email:
        existing = db.query(UserTable).filter_by(
            email=update_user.email
            ).first()


        # se email existir e id for diferente do id do usuário (verificado pelo usuario_logado)
        if existing and existing.id != usuario.id:  
            raise HTTPException(status_code = 400, detail = "esse email já está em uso")


        usuario.email = update_user.email


    # mudança de senha
    if update_user.senha:
        usuario.senha = argon_context.hash(update_user.senha)   # criptografando a nova senha


    db.commit()
    db.refresh(usuario)    # atualizando usuario para as mudanças já serem realizadas no banco
    
    
    return resposta_sucesso(    # success já vem como True pela função
        f"dados do usuário atualizados com sucesso!",   
        {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email
        }
    )
    
    
   
@profile_router.delete("/excluir_conta", response_model=CommonResponse)
async def excluir_usuario(
                    db: Session = Depends(get_db),
                    usuario_id: int = Depends(usuario_logado)
                    ):
    
    
    # pedido a ser cancelado
    usuario = db.query(UserTable).filter_by(
        id=usuario_id
        ).first()
    
    
    if not usuario:
        raise HTTPException(status_code=404, detail="usuario não encontrado")
    
    usuario_excluido = ExcludedUserTable(
        id_utilizado = usuario.id,
        nome = usuario.nome,
        email = usuario.email,
        senha = usuario.senha,
    )  
    
    
    db.add(usuario_excluido)    # Inserindo o usuário na tabela de usuários excluídos para manter histórico
    db.delete(usuario)    # deletando usuário da tabela de usuários
    
    db.commit()


    return resposta_sucesso(  # success já vem como True pela função
        "usuario excluído com sucesso", 
        {
            "id": usuario.id,
            "nome": usuario.nome
        }
    ) 
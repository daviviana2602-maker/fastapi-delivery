# services para as rotas de Perfil

from sqlalchemy.orm import Session

from db.models import UserTable, OrderTable, STATUS_USUARIO_VALIDOS

from schemas import UpdateProfileSchema

from helpers import resposta_sucesso

from security import argon_context

from fastapi import HTTPException



def editar_perfil_services(
                    update_user: UpdateProfileSchema,
                    usuario_id: int,
                    db: Session
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


    try:
        db.commit()
        db.refresh(usuario)    # atualizando usuario para as mudanças já serem realizadas no banco
    except Exception:
        db.rollback()
        raise
    
    
    return resposta_sucesso(    # success já vem como True pela função
        f"dados do usuário atualizados com sucesso!",   
        {
            "id": usuario.id,
            "nome": usuario.nome,
            "email": usuario.email
        }
    )
    
    
   
def excluir_usuario_services(
                    senha_atual: str,
                    db: Session,
                    usuario_id: int
                    ):


    # pedido a ser cancelado
    usuario = db.query(UserTable).filter_by(
        id=usuario_id
        ).first()
    
    
    if not usuario:
        raise HTTPException(status_code=404, detail="usuario não encontrado")
    
    
    if not senha_atual:
        raise HTTPException(status_code = 400, detail = "senha atual é obrigatória para exclusão de conta")
    
    
    if not argon_context.verify(senha_atual, usuario.senha):    # verifica se a senha está correta, mesmo estando criptografada por comparação de hash
            raise HTTPException(status_code = 400, detail = "senha atual inválida")
    
    
    # verifica se o usuário que quer excluir a conta tem algum pedido pendente
    pedido_ativo = db.query(OrderTable).filter(     
                OrderTable.usuario_id == usuario_id,
                OrderTable.status == "PENDENTE"
                ).first()


    # Caso tenha
    if pedido_ativo:
        raise HTTPException(status_code=400, detail="Finalize ou cancele pedidos antes de excluir a conta.")
        
    usuario.status = "EXCLUIDO"
    
    try:
        db.commit()
        db.refresh(usuario)
    except Exception:
        db.rollback()
        raise


    return resposta_sucesso(  # success já vem como True pela função
        "usuario excluído com sucesso", 
        {
            "id": usuario.id,
            "nome": usuario.nome
        }
    ) 
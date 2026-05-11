from fastapi import HTTPException, Depends

from sqlalchemy.orm import Session

from dependencies import get_db, usuario_logado

from db.models import UserTable

import resend

from config import RESEND_API_KEY
resend.api_key = RESEND_API_KEY


# Não é uma dependência, porque depende de recurso_usuario_id, que muda dependendo da utilização
def checar_dono_ou_admin(
    recurso_usuario_id: int,  # id do dono do recurso (pedido, item, etc)
    usuario_id: int = Depends(usuario_logado),
    db: Session = Depends(get_db)
):
    
    usuario = db.query(UserTable).filter_by(
        id=usuario_id
        ).first()
    
    if not usuario:
        raise HTTPException(status_code=401, detail="Usuário não encontrado")

    if recurso_usuario_id != usuario_id and not usuario.admin:
        raise HTTPException(status_code=403, detail="Você não tem permissão")   # se não for o dono do recurso e nem adm

    return True


# modelo de respostas padronizadas
def resposta_sucesso(msg: str, data=None):
    response = {
        "success": True,
        "msg": msg
    }

    if data is not None:
        response["data"] = data    # se data não for vazio é inserido no response

    return response


# função para envio de email (recuperação de conta)
def reset_email(to_email: str, token: str):

    reset_link = f"http://localhost:5500/pages/reset-senha.html?token={token}"

    resend.Emails.send({
        "from": "onboarding@resend.dev",
        "to": [to_email],
        "subject": "Recuperação de senha",
        "html": f"""
            <h1>Recuperação de senha</h1>

            <a href="{reset_link}">
                Redefinir senha
            </a>
        """
    })
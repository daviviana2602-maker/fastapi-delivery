# Autenticação
from fastapi import APIRouter

auth_router = APIRouter(prefix = "/auth", tags=["auth"])   # define o caminho = domínio/auth/(rota esolhinha)


@auth_router.get("/")
async def pedidos():
    return {
            "msg": "você entrou na tela de autenticação",
            "msg2": "está tudo ok"
            }
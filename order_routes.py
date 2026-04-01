# Pedidos
from fastapi import APIRouter

order_router = APIRouter(prefix = "/order", tags=["order"])   # define o caminho = domínio/order/(rota esolhinha)


@order_router.get("/")
async def pedidos():
    return {"msg": "você entrou na tela de pedidos"}
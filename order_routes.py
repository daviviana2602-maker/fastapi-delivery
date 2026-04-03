# Pedidos
from pydantic import EmailStr

from sqlalchemy.orm import Session

from dependencies import get_db

from models import UserTable

from security import argon_context

from fastapi import APIRouter, Depends


order_router = APIRouter(prefix = "/order", tags=["order"])   # define o caminho = domínio/order/(rota esolhinha)



@order_router.get("/")   # rota de entrada (inicial)
async def pedidos():
    return {"msg": "você entrou na tela de pedidos"}
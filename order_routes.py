# Pedidos
from pydantic import EmailStr

from sqlalchemy.orm import Session

from dotenv import load_dotenv
import os
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

from dependencies import get_db

from models import UserTable

from security import bcrypt_context

from fastapi import APIRouter, Depends


order_router = APIRouter(prefix = "/order", tags=["order"])   # define o caminho = domínio/order/(rota esolhinha)


@order_router.get("/")
async def pedidos():
    return {"msg": "você entrou na tela de pedidos"}
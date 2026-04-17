from fastapi import FastAPI

from contextlib import asynccontextmanager

from populate_db import popular_cardapio


# rodando a função de popular cardápio (quando o sistema inicia)
@asynccontextmanager
async def lifespan(app: FastAPI):
    popular_cardapio()      # ANTES do yield → STARTUP (roda quando sistema inicia)
    yield
    # DEPOIS do yield → SHUTDOWN (roda quando o sistema é finalizado)
    

app = FastAPI(lifespan=lifespan) # python -m uvicorn main:app --reload para iniciar LOCALMENTE


from auth_routes import auth_router     # importando rotas de autenticação
from order_routes import order_router   # importando rotas de pedidos
from management_routes import management_router   # importando rotas de administração
from profile_routes import profile_router   # importando rotas de perfil


# inserindo as rotas no app
app.include_router(auth_router)
app.include_router(order_router)  
app.include_router(management_router)  
app.include_router(profile_router)
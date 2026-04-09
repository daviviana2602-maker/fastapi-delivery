# Arquivo Principal

from fastapi import FastAPI

from populate_db import popular_cardapio


app = FastAPI()     # python -m uvicorn main:app --reload

import models
models.Base.metadata.create_all(bind=models.engine)     # Criando tabelas no db


# Popular cardápio só na inicialização do app
@app.on_event("startup")    # "startup" → função roda uma vez quando o servidor abre. (tem também "shutdown" função roda uma vez quando o servidor vai fechar)
def startup_popular_cardapio():
    popular_cardapio()
    
    
from auth_routes import auth_router    # chamando as rotas de autenticação
from order_routes import order_router   # chamando as rotas de pedidos
from management_routes import management_router     # chamando as rotas de administração


# Registro dos routers no app principal. Isso integra as rotas ao sistema e as torna acessíveis via HTTP
app.include_router(auth_router)
app.include_router(order_router)  
app.include_router(management_router)  
# Arquivo Principal

from fastapi import FastAPI

import models
models.Base.metadata.create_all(bind=models.engine)     # Criando tabelas no db


app = FastAPI()     # python -m uvicorn main:app --reload


from auth_routes import auth_router    # chamando as rotas de autenticação
from order_routes import order_router   # chamando as rotas de pedidos
from management_routes import management_router     # chamando as rotas de administração


# Registro dos routers no app principal. Isso integra as rotas ao sistema e as torna acessíveis via HTTP
app.include_router(auth_router)
app.include_router(order_router)  
app.include_router(management_router)  
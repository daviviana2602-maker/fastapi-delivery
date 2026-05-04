from fastapi import FastAPI
from contextlib import asynccontextmanager

from db.populate_db import popular_cardapio
from fastapi.middleware.cors import CORSMiddleware

from routes.auth_routes import auth_router
from routes.order_routes import order_router
from routes.management_routes import management_router
from routes.profile_routes import profile_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    popular_cardapio()      # ANTES do yield → STARTUP (roda quando sistema inicia)
    yield
    # DEPOIS do yield → SHUTDOWN (roda quando o sistema é finalizado)
    

app = FastAPI(lifespan=lifespan) # python -m uvicorn main:app --reload para iniciar LOCALMENTE


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth_router)
app.include_router(order_router)  
app.include_router(management_router)  
app.include_router(profile_router)
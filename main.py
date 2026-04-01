from fastapi import FastAPI, Depends
from pydantic import BaseModel, EmailStr, Field


from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session


import models
models.Base.metadata.create_all(bind=models.engine)


app = FastAPI()     # python -m uvicorn main:app --reload

from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)    
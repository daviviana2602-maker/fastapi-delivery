# Criação de Esquemas

from typing import Annotated
from pydantic import BaseModel, EmailStr, Field



class CreateUserSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    
    # Faz não ser transformado em um dicionário Python comum, assim sendo melhor interpretado pelo SQLAlchemy
    class Config:
        from_attributes = True
        
        

class OrderSchema(BaseModel):
    usuario_id: int
    
    # Faz não ser transformado em um dicionário Python comum, assim sendo melhor interpretado pelo SQLAlchemy
    class Config:
        from_attributes = True
        
        
     
class LoginSchema(BaseModel):
    email: EmailStr
    senha: str
    
    # Faz não ser transformado em um dicionário Python comum, assim sendo melhor interpretado pelo SQLAlchemy
    class Config:
        from_attributes = True   
        
        

class TokenSchema(BaseModel):
    refresh_token: str
    
    # Faz não ser transformado em um dicionário Python comum, assim sendo melhor interpretado pelo SQLAlchemy
    class Config:
        from_attributes = True   
        
        
        
class AlterationUserSchema(BaseModel):
    usuario_a_sofrer_alteracao: int   
    
    # Faz não ser transformado em um dicionário Python comum, assim sendo melhor interpretado pelo SQLAlchemy
    class Config:
        from_attributes = True
        
        
        
class AddItemSchema(BaseModel):
    quantidade: Annotated[int, Field(gt=0)]   # garante que seja > 0 
    nome: str
    tamanho: str
    pedido_id: int  # diz qual pedido você pretende adicionar
    
    # Faz não ser transformado em um dicionário Python comum, assim sendo melhor interpretado pelo SQLAlchemy
    class Config:
        from_attributes = True
        
        

class AdjustItemSchema(BaseModel):
    item_id: int    # comparar id com o da TempItemsTable
    ajuste: int     # quantidade de itens a serem removidos ou adicionados (positivo/negativo)
        
    # Faz não ser transformado em um dicionário Python comum, assim sendo melhor interpretado pelo SQLAlchemy
    class Config:
        from_attributes = True
        
        
        
class FinishOrderSchema(BaseModel):
    pedido_id: int
    
    # Faz não ser transformado em um dicionário Python comum, assim sendo melhor interpretado pelo SQLAlchemy
    class Config:
        from_attributes = True
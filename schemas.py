from typing import Annotated

from pydantic import BaseModel, EmailStr, Field

from typing import Optional


class CreateUserSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str
        
        

class OrderSchema(BaseModel):
    usuario_id: int
        
        
     
class LoginSchema(BaseModel):
    email: EmailStr
    senha: str   
        
        

class TokenSchema(BaseModel):
    refresh_token: str   
        
        
        
class AlterationUserSchema(BaseModel):
    usuario_a_sofrer_alteracao: int   
        
        
        
class AddItemSchema(BaseModel):
    quantidade: Annotated[int, Field(gt=0)]   # garante que seja > 0 
    nome: str
    tamanho: str
    pedido_id: int    
        
        

class AdjustItemSchema(BaseModel):
    item_id: int    # comparar id com o da TempItemsTable
    ajuste: int     # quantidade de itens a serem removidos ou adicionados (positivo/negativo)

        
        
        
class FinishOrderSchema(BaseModel):
    pedido_id: int
        
        
        
class UpdateProfileSchema(BaseModel):
    nome: Optional[str] = None
    email: Optional[EmailStr] = None
    senha: Optional[str] = None
    senha_atual: Optional[str] = None
# Criação de Esquemas

from pydantic import BaseModel, EmailStr



class UserSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    ativo: bool = True
    admin: bool = False
    
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
        


class CancelPedidoSchema(BaseModel):
    pedido_id: int
    
    # Faz não ser transformado em um dicionário Python comum, assim sendo melhor interpretado pelo SQLAlchemy
    class Config:
        from_attributes = True
        
        
        
class PromoteUserSchema(BaseModel):
    usuario_a_promover_id: int   
    
    # Faz não ser transformado em um dicionário Python comum, assim sendo melhor interpretado pelo SQLAlchemy
    class Config:
        from_attributes = True
        
        
        
class DemoteUserSchema(BaseModel):
    usuario_a_rebaixar_id: int   
    
    # Faz não ser transformado em um dicionário Python comum, assim sendo melhor interpretado pelo SQLAlchemy
    class Config:
        from_attributes = True
        
        

class DeleteUserSchema(BaseModel):
    usuario_a_deletar_id: int   
    
    # Faz não ser transformado em um dicionário Python comum, assim sendo melhor interpretado pelo SQLAlchemy
    class Config:
        from_attributes = True
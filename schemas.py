from pydantic import BaseModel, EmailStr

from typing import Optional


# Feito com base nas tabelas do models.py
class UserSchema(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    ativo: Optional[bool]
    admin: Optional[bool]
    
    # Faz não ser transformado em um dicionário Python comum, assim sendo melhor interpretado pelo SQLAlchemy
    class Config:
        from_attributes = True
        
        
# Feito com base nas tabelas do models.py
class OrderSchema(BaseModel):
    usuario_id: int
    
    # Faz não ser transformado em um dicionário Python comum, assim sendo melhor interpretado pelo SQLAlchemy
    class Config:
        from_attributes = True
# Schemas para respostas mais organizadas e padronizadas

from pydantic import BaseModel
from typing import Optional, Any



class CommonResponse(BaseModel):
    success: bool
    msg: str
    data: Optional[Any] = None  # não retorna None (pois data é opcional) e se existir pode ser de qualquer tipo (str, int, float, objeto ...)
    
    # Faz não ser transformado em um dicionário Python comum, assim sendo melhor interpretado pelo SQLAlchemy
    class Config:
        from_attributes = True
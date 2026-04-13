# Esquemas para respostas mais organizadas e padronizadas

from pydantic import BaseModel
from typing import Optional, Any



class CommonResponse(BaseModel):
    success: bool
    msg: str
    data: Optional[Any] = None  # não retorna None (pois data é opcional) e se existir pode ser de qualquer tipo (str, int, float, objeto ...)
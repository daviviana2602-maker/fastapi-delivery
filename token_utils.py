from jose import jwt, JWTError

from config import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY

from datetime import datetime, timedelta, timezone

from fastapi import HTTPException

from db.models import UserTable


def criar_token(usuario_id, duracao_token=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):   
    prazo_token = datetime.now(timezone.utc) + duracao_token    
    dic_infos = {
        "sub": str(usuario_id),  # identificador do dono do token (transformar em string sempre e nome "sub" é padrão JWT)
        "exp": prazo_token  
    }
    
    jwt_codificado = jwt.encode(dic_infos, SECRET_KEY, ALGORITHM)    # Gerando token JWT a partir dos dados do usuário, assinado com a SECRET_KEY

    return jwt_codificado
    


def verificar_token(token: str, db):
    try:
        jwt_decodificado = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])    
        usuario_id = jwt_decodificado.get("sub")

        usuario = db.query(UserTable).filter(
            UserTable.id == usuario_id
            ).first()
        
        if not usuario:
            raise HTTPException(status_code=401, detail="usuário não encontrado")
        
        return jwt_decodificado

    except JWTError:
        raise HTTPException(status_code=401, detail="token inválido ou expirado")  
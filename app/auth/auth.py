
from fastapi import Header, HTTPException

API_KEY = "123456"

def verificar_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token não enviado")

    token = authorization.replace("Bearer ", "")

    if len(token) < 10:
        raise HTTPException(status_code=401, detail="Token inválido")

    return token

def verificar_api_key(x_api_key: str = Header(None)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="API Key inválida")


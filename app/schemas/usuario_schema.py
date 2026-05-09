
from pydantic import BaseModel

class UsuarioCreate(BaseModel):
    email: str
    senha: str

class Login(BaseModel):
    email: str
    senha: str

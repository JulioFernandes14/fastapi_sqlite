
from fastapi import FastAPI, Depends
from app.controllers import usuario_controller
from app.schemas.usuario_schema import UsuarioCreate, Login
from app.auth.auth import verificar_token

app = FastAPI()

@app.get("/")
def home():
    return {"msg": "API rodando"}

@app.get("/usuarios")
def listar_usuarios():
    return usuario_controller.listar()

@app.post("/cadastro")
def cadastro(user: UsuarioCreate):
    return usuario_controller.cadastrar(user.email, user.senha)

@app.post("/login")
def login(user: Login):
    return usuario_controller.login(user.email, user.senha)

@app.get("/perfil")
def perfil(token: str = Depends(verificar_token)):
    return {"msg": "Usuário autenticado"}

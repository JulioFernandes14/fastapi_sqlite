from fastapi import FastAPI
from app.controllers import usuario_controller
from app.schemas.usuario_schema import UsuarioCreate

app = FastAPI()


@app.get("/")
def home():
    return {"msg": "API funcionando 🚀"}


@app.get("/usuarios")
def listar_usuarios():
    return usuario_controller.listar()


@app.post("/usuarios")
def criar_usuario(usuario: UsuarioCreate):
    return usuario_controller.criar(usuario.nome)

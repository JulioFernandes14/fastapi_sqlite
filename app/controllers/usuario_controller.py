
from app.models import usuario_model
from app.views import usuario_view

def listar():
  usuarios = usuario_model.listar_usuarios()
  return usuario_view.resposta_sucesso("Lista de usuários", usuarios)

def cadastrar(email, senha):
    return usuario_model.cadastrar_usuario(email, senha)

def login(email, senha):
    return usuario_model.login_usuario(email, senha)


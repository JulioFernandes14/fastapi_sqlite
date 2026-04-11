from app.models import usuario_model
from app.views import usuario_view


def listar():
    usuarios = usuario_model.listar_usuarios()
    return usuario_view.resposta_sucesso("Lista de usuários", usuarios)


def criar(nome):
    usuario = usuario_model.criar_usuario(nome)
    return usuario_view.resposta_sucesso("Usuário criado", usuario)

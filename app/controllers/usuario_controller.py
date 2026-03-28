from app.models import usuario_model
from app.views import usuario_view


def listar_usuarios():
    return usuario_model.listar()


def criar_usuario(nome):
    usuario_model.criar(nome)
    return usuario_view.resposta_sucesso("Usuário criado")
          
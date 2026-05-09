import bcrypt
import jwt
import os

from datetime import datetime, timedelta
from dotenv import load_dotenv

from app.database.supabase_client import supabase

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
EXPIRATION_MINUTES = int(os.getenv("EXPIRATION_MINUTES", 60))

ALGORITHM = "HS256"


def listar_usuarios():
    response = supabase.table("usuarios").select("*").execute()
    return response.data


def buscar_usuario_por_email(email):
    response = (
        supabase
        .table("usuarios")
        .select("*")
        .eq("email", email)
        .execute()
    )

    usuarios = response.data

    return usuarios[0] if usuarios else None


def cadastrar_usuario(email, senha):
    if buscar_usuario_por_email(email):
        raise Exception("Já existe um usuário cadastrado com este email.")

    senha_hash = bcrypt.hashpw(
        senha.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    response = (
        supabase
        .table("usuarios")
        .insert({
            "email": email,
            "senha": senha_hash
        })
        .execute()
    )

    usuario_criado = response.data[0]

    return {
        "mensagem": "Usuário cadastrado com sucesso.",
        "usuario": {
            "id": usuario_criado.get("id"),
            "email": usuario_criado.get("email")
        }
    }


def gerar_token(usuario_id, email):
    payload = {
        "sub": str(usuario_id),
        "email": email,
        "exp": datetime.utcnow() + timedelta(minutes=EXPIRATION_MINUTES)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def login_usuario(email, senha):
    usuario = buscar_usuario_por_email(email)

    if not usuario:
        raise Exception("Email ou senha inválidos.")

    senha_hash = usuario.get("senha")

    if not bcrypt.checkpw(
        senha.encode("utf-8"),
        senha_hash.encode("utf-8")
    ):
        raise Exception("Email ou senha inválidos.")

    token = gerar_token(
        usuario.get("id"),
        usuario.get("email")
    )

    return {
        "mensagem": "Login realizado com sucesso.",
        "token": token,
        "usuario": {
            "id": usuario.get("id"),
            "email": usuario.get("email")
        }
    }
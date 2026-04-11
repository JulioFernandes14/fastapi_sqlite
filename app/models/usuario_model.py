

from app.database.supabase_client import supabase

def listar_usuarios():
    response = supabase.table("usuarios").select("*").execute()
    return response.data

def criar_usuario(nome):
    response = supabase.table("usuarios").insert({"nome": nome}).execute()
    return response.data 
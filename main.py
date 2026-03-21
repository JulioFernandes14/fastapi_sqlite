from fastapi import FastAPI
import sqlite3

# IMPORTANTE: executa a criação do banco/tabela
import app.database.db

app = FastAPI()


def get_connection():
    return sqlite3.connect("database.db")


@app.get("/")
def home():
    return {"msg": "API rodando"}


@app.get("/usuarios")
def listar_usuarios():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios")
    dados = cursor.fetchall()

    conn.close()
    return list(map(lambda dado: {"id": dado[0], "nome": dado[1], "idade": dado[2]}, dados))


@app.post("/usuarios")
def criar_usuario(nome: str, idade: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("INSERT INTO usuarios (nome, idade) VALUES (?, ?)", (nome, idade))

    conn.commit()
    conn.close()

    return {"msg": "Usuário criado"}


@app.delete("/usuarios/{id}")
def deletar_usuario(id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id, ))

    conn.commit()
    conn.close()

    return {"msg": "Usuário deletado"}


@app.put("/usuarios/{id}")
def atualizar_nome_usuario(id: int, nome: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(f"UPDATE usuarios SET nome = ? WHERE id = ?", (nome, id,))

    conn.commit()
    conn.close()

    return {"msg": "Nome do usuário alterado"}

@app.get("/usuarios/{id}")
def buscar_usuario(id: int):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM usuarios where id = ?", (id,))
    dado = cursor.fetchone()
    
    conn.close()
    
    return {
        "id": dado[0],
        "nome": dado[1],
        "idade": dado[2]
    }



@app.delete("/usuarios/clean")
def limpar_usuarios():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM usuarios")
    conn.commit()
    conn.close()

    return {"msg": "Todos os usuários foram deletados"}

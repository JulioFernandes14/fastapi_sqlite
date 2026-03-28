from fastapi import FastAPI, HTTPException
from typing import Optional
import sqlite3

# IMPORTANTE: executa a criação do banco/tabela
import app.database.db

app = FastAPI()


def get_connection():
    return sqlite3.connect("database.db")


@app.get("/")
def home():
    return {"msg": "API rodando"}


# USUARIOS


@app.get("/usuarios")
def listar_usuarios():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios")
    dados = cursor.fetchall()

    conn.close()
    return list(
        map(lambda dado: {"id": dado[0], "nome": dado[1], "idade": dado[2]}, dados)
    )


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

    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id,))

    conn.commit()
    conn.close()

    return {"msg": "Usuário deletado"}


@app.put("/usuarios/{id}")
def atualizar_nome_usuario(id: int, nome: str):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        f"UPDATE usuarios SET nome = ? WHERE id = ?",
        (
            nome,
            id,
        ),
    )

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

    return {"id": dado[0], "nome": dado[1], "idade": dado[2]}


@app.delete("/usuarios/clean")
def limpar_usuarios():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM usuarios")
    conn.commit()
    conn.close()

    return {"msg": "Todos os usuários foram deletados"}


# PRODUTOS


@app.post("/produtos")
def criar_produto(nome: str, categoria: str, valor: float):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO produtos (nome, categoria, valor) VALUES (?, ?,?)",
        (nome, categoria, valor),
    )

    conn.commit()
    conn.close()

    return {"msg": "Produto criado"}


@app.get("/produtos")
def listar_produtos(
    categoria: Optional[str] = None,
    preco_min: Optional[float] = None,
    preco_max: Optional[float] = None,
):
    conn = get_connection()
    cursor = conn.cursor()

    query = "SELECT * FROM produtos WHERE 1=1"
    params = []

    if (preco_min and preco_max):
        if(preco_max < preco_min):
            raise HTTPException(status_code=400, detail="Preço máximo deve ser maior que preço mínimo")

    if categoria:
        query += " AND categoria = ?"
        params.append(categoria)

    if preco_min:
        query += " AND preco >= ?"
        params.append(preco_min)

    if preco_max:
        query += " AND preco <= ?"
        params.append(preco_max)

    cursor.execute(query, tuple(params))
    dados = cursor.fetchall()

    conn.close()
    return dados

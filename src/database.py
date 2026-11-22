import sqlite3
from pathlib import Path

DATABASE = Path(__file__).resolve().parent.parent / "techflow.db"


def conectar():
    conexao = sqlite3.connect(DATABASE)
    conexao.row_factory = sqlite3.Row
    return conexao


def criar_tabela():
    conexao = conectar()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            status TEXT NOT NULL DEFAULT 'A Fazer',
            prioridade TEXT NOT NULL DEFAULT 'Média'
        )
    """)

    # Verifica se a coluna prioridade já existe
    colunas = conexao.execute(
        "PRAGMA table_info(tarefas)"
    ).fetchall()

    nomes_colunas = [coluna["name"] for coluna in colunas]

    # Adiciona prioridade em bancos criados anteriormente
    if "prioridade" not in nomes_colunas:
        conexao.execute("""
            ALTER TABLE tarefas
            ADD COLUMN prioridade TEXT NOT NULL DEFAULT 'Média'
        """)

    conexao.commit()
    conexao.close()
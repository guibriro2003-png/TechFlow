
import sqlite3
from pathlib import Path

# Define o caminho do banco de dados na pasta principal
DATABASE = Path(__file__).resolve().parent.parent / "techflow.db"


# Cria a conexão com o banco de dados
def conectar():
    conexao = sqlite3.connect(DATABASE)
    conexao.row_factory = sqlite3.Row
    return conexao


# Cria a tabela de tarefas caso ela não exista
def criar_tabela():
    conexao = conectar()

    conexao.execute("""
        CREATE TABLE IF NOT EXISTS tarefas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            status TEXT NOT NULL DEFAULT 'A Fazer'
        )
    """)

    conexao.commit()
    conexao.close()

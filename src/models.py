
from database import conectar


# Cadastra uma nova tarefa
def criar_tarefa(titulo, descricao):
    conexao = conectar()

    conexao.execute(
        """
        INSERT INTO tarefas (titulo, descricao)
        VALUES (?, ?)
        """,
        (titulo, descricao)
    )

    conexao.commit()
    conexao.close()


# Lista todas as tarefas
def listar_tarefas():
    conexao = conectar()

    tarefas = conexao.execute(
        "SELECT * FROM tarefas ORDER BY id DESC"
    ).fetchall()

    conexao.close()
    return tarefas


# Atualiza uma tarefa existente
def atualizar_tarefa(id, titulo, descricao, status):
    conexao = conectar()

    conexao.execute(
        """
        UPDATE tarefas
        SET titulo = ?, descricao = ?, status = ?
        WHERE id = ?
        """,
        (titulo, descricao, status, id)
    )

    conexao.commit()
    conexao.close()


# Exclui uma tarefa
def excluir_tarefa(id):
    conexao = conectar()

    conexao.execute(
        "DELETE FROM tarefas WHERE id = ?",
        (id,)
    )

    conexao.commit()
    conexao.close()

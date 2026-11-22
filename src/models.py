from database import conectar


def criar_tarefa(titulo, descricao, prioridade="Média"):
    conexao = conectar()

    conexao.execute(
        """INSERT INTO tarefas (titulo, descricao, prioridade)
           VALUES (?, ?, ?)""",
        (titulo, descricao, prioridade)
    )

    conexao.commit()
    conexao.close()


def listar_tarefas(prioridade=None):
    conexao = conectar()

    if prioridade:
        tarefas = conexao.execute(
            """SELECT * FROM tarefas
               WHERE prioridade = ?
               ORDER BY id DESC""",
            (prioridade,)
        ).fetchall()
    else:
        tarefas = conexao.execute(
            "SELECT * FROM tarefas ORDER BY id DESC"
        ).fetchall()

    conexao.close()
    return tarefas


def atualizar_tarefa(id, titulo, descricao, status, prioridade="Média"):
    conexao = conectar()

    conexao.execute(
        """UPDATE tarefas
           SET titulo = ?, descricao = ?, status = ?, prioridade = ?
           WHERE id = ?""",
        (titulo, descricao, status, prioridade, id)
    )

    conexao.commit()
    conexao.close()


def excluir_tarefa(id):
    conexao = conectar()

    conexao.execute(
        "DELETE FROM tarefas WHERE id = ?",
        (id,)
    )

    conexao.commit()
    conexao.close()
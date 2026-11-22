
import sys
from pathlib import Path

# Permite importar os módulos da pasta src
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from database import conectar, criar_tabela
from models import (
    criar_tarefa,
    listar_tarefas,
    atualizar_tarefa,
    excluir_tarefa
)


def limpar_banco():
    conexao = conectar()
    conexao.execute("DELETE FROM tarefas")
    conexao.commit()
    conexao.close()


def test_criar_tarefa():
    criar_tabela()
    limpar_banco()

    criar_tarefa("Estudar Python", "Praticar Flask")

    tarefas = listar_tarefas()

    assert len(tarefas) == 1
    assert tarefas[0]["titulo"] == "Estudar Python"

    limpar_banco()


def test_atualizar_tarefa():
    criar_tabela()
    limpar_banco()

    criar_tarefa("Tarefa antiga", "Descrição")

    tarefa = listar_tarefas()[0]

    atualizar_tarefa(
        tarefa["id"],
        "Tarefa atualizada",
        "Nova descrição",
        "Em Progresso"
    )

    tarefas = listar_tarefas()

    assert tarefas[0]["titulo"] == "Tarefa atualizada"
    assert tarefas[0]["status"] == "Em Progresso"

    limpar_banco()


def test_excluir_tarefa():
    criar_tabela()
    limpar_banco()

    criar_tarefa("Tarefa para excluir", "Teste")

    tarefa = listar_tarefas()[0]

    excluir_tarefa(tarefa["id"])

    tarefas = listar_tarefas()

    assert len(tarefas) == 0

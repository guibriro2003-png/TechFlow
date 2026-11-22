
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import database
from models import atualizar_tarefa, criar_tarefa, excluir_tarefa, listar_tarefas


def test_criar_tarefa(monkeypatch, tmp_path):
    monkeypatch.setattr(database, "DATABASE", tmp_path / "teste.db")
    database.criar_tabela()

    criar_tarefa("Estudar Python", "Praticar Flask", "Média")

    tarefas = listar_tarefas()

    assert len(tarefas) == 1
    assert tarefas[0]["titulo"] == "Estudar Python"
    assert tarefas[0]["prioridade"] == "Média"


def test_atualizar_tarefa(monkeypatch, tmp_path):
    monkeypatch.setattr(database, "DATABASE", tmp_path / "teste.db")
    database.criar_tabela()

    criar_tarefa("Tarefa antiga", "Descrição", "Baixa")
    tarefa = listar_tarefas()[0]

    atualizar_tarefa(
        tarefa["id"],
        "Tarefa atualizada",
        "Nova descrição",
        "Em Progresso",
        "Alta"
    )

    tarefas = listar_tarefas()

    assert tarefas[0]["titulo"] == "Tarefa atualizada"
    assert tarefas[0]["status"] == "Em Progresso"
    assert tarefas[0]["prioridade"] == "Alta"


def test_excluir_tarefa(monkeypatch, tmp_path):
    monkeypatch.setattr(database, "DATABASE", tmp_path / "teste.db")
    database.criar_tabela()

    criar_tarefa("Tarefa para excluir", "Teste")
    tarefa = listar_tarefas()[0]

    excluir_tarefa(tarefa["id"])

    assert len(listar_tarefas()) == 0


def test_filtrar_por_prioridade(monkeypatch, tmp_path):
    monkeypatch.setattr(database, "DATABASE", tmp_path / "teste.db")
    database.criar_tabela()

    criar_tarefa("Tarefa urgente", "Resolver problema", "Alta")
    criar_tarefa("Tarefa normal", "Estudar", "Média")
    criar_tarefa("Tarefa simples", "Organizar arquivos", "Baixa")

    tarefas = listar_tarefas("Alta")

    assert len(tarefas) == 1
    assert tarefas[0]["titulo"] == "Tarefa urgente"
    assert tarefas[0]["prioridade"] == "Alta"

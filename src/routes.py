
from flask import Blueprint, request, redirect, url_for, render_template_string

from models import (
    criar_tarefa,
    listar_tarefas,
    atualizar_tarefa,
    excluir_tarefa
)

# Criando um grupo de rotas
rotas = Blueprint("rotas", __name__)


# Página principal com a lista de tarefas
@rotas.route("/")
def inicio():
    tarefas = listar_tarefas()

    return render_template_string("""
        <h1>TechFlow - Gerenciador de Tarefas</h1>

        <h2>Nova tarefa</h2>

        <form action="/criar" method="POST">
            <input type="text" name="titulo"
                   placeholder="Título da tarefa" required>

            <input type="text" name="descricao"
                   placeholder="Descrição">

            <button type="submit">Cadastrar</button>
        </form>

        <hr>

        <h2>Minhas tarefas</h2>

        {% for tarefa in tarefas %}
            <h3>{{ tarefa['titulo'] }}</h3>
            <p>{{ tarefa['descricao'] }}</p>
            <p>Status: {{ tarefa['status'] }}</p>

            <form action="/atualizar/{{ tarefa['id'] }}"
                  method="POST">
                <input type="text" name="titulo"
                       value="{{ tarefa['titulo'] }}" required>

                <input type="text" name="descricao"
                       value="{{ tarefa['descricao'] or '' }}">

                <select name="status">
                    <option>A Fazer</option>
                    <option>Em Progresso</option>
                    <option>Concluído</option>
                </select>

                <button type="submit">Atualizar</button>
            </form>

            <form action="/excluir/{{ tarefa['id'] }}"
                  method="POST">
                <button type="submit">Excluir</button>
            </form>

            <hr>
        {% else %}
            <p>Nenhuma tarefa cadastrada.</p>
        {% endfor %}
    """, tarefas=tarefas)


# Rota para cadastrar tarefa
@rotas.route("/criar", methods=["POST"])
def criar():
    titulo = request.form.get("titulo", "").strip()
    descricao = request.form.get("descricao", "").strip()

    if titulo:
        criar_tarefa(titulo, descricao)

    return redirect(url_for("rotas.inicio"))


# Rota para atualizar tarefa
@rotas.route("/atualizar/<int:id>", methods=["POST"])
def atualizar(id):
    titulo = request.form.get("titulo", "").strip()
    descricao = request.form.get("descricao", "").strip()
    status = request.form.get("status", "A Fazer")

    if titulo and status in ["A Fazer", "Em Progresso", "Concluído"]:
        atualizar_tarefa(id, titulo, descricao, status)

    return redirect(url_for("rotas.inicio"))


# Rota para excluir tarefa
@rotas.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    excluir_tarefa(id)
    return redirect(url_for("rotas.inicio"))

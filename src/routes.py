
from flask import Blueprint, request, redirect, url_for, render_template_string

from models import (
    criar_tarefa,
    listar_tarefas,
    atualizar_tarefa,
    excluir_tarefa
)

rotas = Blueprint("rotas", __name__)

PRIORIDADES = ["Baixa", "Média", "Alta"]
STATUS = ["A Fazer", "Em Progresso", "Concluído"]


# Página principal
@rotas.route("/")
def inicio():
    prioridade_filtro = request.args.get("prioridade", "").strip()

    if prioridade_filtro not in PRIORIDADES:
        prioridade_filtro = ""

    tarefas = listar_tarefas(prioridade_filtro or None)

    return render_template_string("""
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <title>TechFlow - Gerenciador de Tarefas</title>

            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 850px;
                    margin: 30px auto;
                    padding: 20px;
                    background: #f4f4f4;
                }

                .tarefa {
                    background: white;
                    padding: 15px;
                    margin: 15px 0;
                    border-radius: 8px;
                    border-left: 6px solid #888;
                }

                .alta {
                    border-left-color: #e53935;
                    background: #fff0f0;
                }

                .media {
                    border-left-color: #f9a825;
                }

                .baixa {
                    border-left-color: #43a047;
                }

                input, select, button {
                    padding: 9px;
                    margin: 5px 0;
                }

                button {
                    cursor: pointer;
                }

                .filtro, .cadastro {
                    background: white;
                    padding: 15px;
                    border-radius: 8px;
                    margin-bottom: 20px;
                }
            </style>
        </head>

        <body>

            <h1>TechFlow - Gerenciador de Tarefas</h1>

            <div class="cadastro">
                <h2>Nova tarefa</h2>

                <form action="/criar" method="POST">
                    <input type="text" name="titulo"
                           placeholder="Título da tarefa" required>

                    <input type="text" name="descricao"
                           placeholder="Descrição">

                    <select name="prioridade">
                        <option value="Baixa">Baixa</option>
                        <option value="Média" selected>Média</option>
                        <option value="Alta">Alta</option>
                    </select>

                    <button type="submit">Cadastrar</button>
                </form>
            </div>

            <div class="filtro">
                <h2>Filtrar tarefas por prioridade</h2>

                <form action="/" method="GET">
                    <select name="prioridade">
                        <option value="">Todas as prioridades</option>

                        {% for prioridade in prioridades %}
                            <option value="{{ prioridade }}"
                                {% if prioridade_filtro == prioridade %}
                                    selected
                                {% endif %}>
                                {{ prioridade }}
                            </option>
                        {% endfor %}
                    </select>

                    <button type="submit">Filtrar</button>
                    <a href="/">Limpar filtro</a>
                </form>
            </div>

            <h2>Minhas tarefas</h2>

            {% for tarefa in tarefas %}

                <div class="tarefa {{ tarefa['prioridade'] | lower }}">

                    <h3>{{ tarefa['titulo'] }}</h3>

                    <p>{{ tarefa['descricao'] }}</p>

                    <p>Status: {{ tarefa['status'] }}</p>

                    <p>
                        Prioridade:
                        <strong>{{ tarefa['prioridade'] }}</strong>

                        {% if tarefa['prioridade'] == 'Alta' %}
                            - TAREFA CRÍTICA
                        {% endif %}
                    </p>

                    <form action="/atualizar/{{ tarefa['id'] }}"
                          method="POST">

                        <input type="text" name="titulo"
                               value="{{ tarefa['titulo'] }}" required>

                        <input type="text" name="descricao"
                               value="{{ tarefa['descricao'] or '' }}">

                        <select name="status">
                            {% for status_opcao in status_opcoes %}
                                <option value="{{ status_opcao }}"
                                    {% if tarefa['status'] == status_opcao %}
                                        selected
                                    {% endif %}>
                                    {{ status_opcao }}
                                </option>
                            {% endfor %}
                        </select>

                        <select name="prioridade">
                            {% for prioridade in prioridades %}
                                <option value="{{ prioridade }}"
                                    {% if tarefa['prioridade'] == prioridade %}
                                        selected
                                    {% endif %}>
                                    {{ prioridade }}
                                </option>
                            {% endfor %}
                        </select>

                        <button type="submit">Atualizar</button>
                    </form>

                    <form action="/excluir/{{ tarefa['id'] }}"
                          method="POST">

                        <button type="submit">Excluir</button>
                    </form>

                </div>

            {% else %}
                <p>Nenhuma tarefa cadastrada.</p>
            {% endfor %}

        </body>
        </html>
    """,
    tarefas=tarefas,
    prioridades=PRIORIDADES,
    prioridade_filtro=prioridade_filtro,
    status_opcoes=STATUS
    )


# Cadastrar tarefa
@rotas.route("/criar", methods=["POST"])
def criar():
    titulo = request.form.get("titulo", "").strip()
    descricao = request.form.get("descricao", "").strip()
    prioridade = request.form.get("prioridade", "Média")

    if titulo and prioridade in PRIORIDADES:
        criar_tarefa(titulo, descricao, prioridade)

    return redirect(url_for("rotas.inicio"))


# Atualizar tarefa
@rotas.route("/atualizar/<int:id>", methods=["POST"])
def atualizar(id):
    titulo = request.form.get("titulo", "").strip()
    descricao = request.form.get("descricao", "").strip()
    status = request.form.get("status", "A Fazer")
    prioridade = request.form.get("prioridade", "Média")

    if (
        titulo
        and status in STATUS
        and prioridade in PRIORIDADES
    ):
        atualizar_tarefa(
            id, titulo, descricao, status, prioridade
        )

    return redirect(url_for("rotas.inicio"))


# Excluir tarefa
@rotas.route("/excluir/<int:id>", methods=["POST"])
def excluir(id):
    excluir_tarefa(id)
    return redirect(url_for("rotas.inicio"))

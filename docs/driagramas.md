
# Diagramas UML - TechFlow

## 1. Diagrama de casos de uso

O diagrama representa as funcionalidades disponíveis para o usuário no sistema.

```mermaid
flowchart TD
    U["Usuário"]

    U --> A(["Cadastrar tarefa"])
    U --> B(["Visualizar tarefas"])
    U --> C(["Editar tarefa"])
    U --> D(["Excluir tarefa"])
    U --> E(["Filtrar por prioridade"])
    U --> F(["Definir prioridade"])

    F --> G(["Baixa"])
    F --> H(["Média"])
    F --> I(["Alta"])
```

## 2. Diagrama de classes

O diagrama representa a organização conceitual dos dados e componentes do TechFlow.

```mermaid
classDiagram
    class Tarefa {
        +int id
        +string titulo
        +string descricao
        +string status
        +string prioridade
    }

    class GerenciadorTarefas {
        +criar_tarefa()
        +listar_tarefas()
        +atualizar_tarefa()
        +excluir_tarefa()
    }

    class BancoDeDados {
        +conectar()
        +criar_tabela()
    }

    class Rotas {
        +pagina_inicial()
        +criar()
        +atualizar()
        +excluir()
    }

    Rotas --> GerenciadorTarefas
    GerenciadorTarefas --> BancoDeDados
    GerenciadorTarefas --> Tarefa
```

## Importância da modelagem

A modelagem UML ajuda a visualizar a estrutura e o funcionamento do sistema antes e durante o desenvolvimento.

No TechFlow, os diagramas permitem compreender as funcionalidades disponíveis ao usuário, os dados armazenados e a relação entre os componentes do projeto.

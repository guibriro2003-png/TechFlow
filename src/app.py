
from flask import Flask

from database import criar_tabela
from routes import rotas

# Inicializando a aplicação
app = Flask(__name__)

# Criando o banco de dados
criar_tabela()

# Registrando as rotas
app.register_blueprint(rotas)


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request
from model.conexao import Base
app = Flask(__name__)

from controller.UsuarioController import *

if __name__ == '__main__':
    Base.metadata.create_all(bind=engine)
    app.run()



# exemplo de uma rota devolvendo apenas um texto.
@app.route('/', methods=['GET'])
def hello_world():  # put application's code here
    return 'Hello World!'

# exemplo de uma rota que devolve um pagina de um template.
@app.route('/pagina', methods=['GET'])
def home():
    return render_template("index.html")

# exemplo de uma rota que trata dados de um formulário html
@app.route('/novo', methods=['POST'])
def hello_world_k():  # put application's code here
    #acessar o BD e salvar essa informação no BD
    #funcao do banck-end, receber os dados, tratar, fazer validações, pessitir os dados
    # recuperar dados persistidos.

    return 'novo PWII: ' + request.form['nome'] + request.form['aniversario']


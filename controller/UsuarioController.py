from app import app
from flask import render_template, request, jsonify, redirect, url_for

from sqlalchemy.orm import sessionmaker

from model.conexao import engine

from model.Usuario import Usuario

Sessionlocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@app.route("/usuarios", methods = ["GET"])
def usuarios():
    db = Sessionlocal()
    usuarios = db.query(Usuario).all()
    return jsonify([usuario.to_dict() for usuario in usuarios]), 200


# exemplo de uma rota que devolve um pagina de um template.
@app.route('/usuarios/novo', methods=['GET'])
def novo():
    db = Sessionlocal()
    usuarios = db.query(Usuario).all();
    return render_template("index.html", obj = usuarios)


@app.route('/usuarios/salvar', methods=['POST'])
def create():
    db = Sessionlocal()
    usuario = Usuario(nome = request.form['nome'], data = request.form['aniversario'])
    db.add(usuario)
    db.commit()
    msg = "Salvo com sucesso!"
    return redirect(url_for('novo', msg = msg))
    #return jsonify({'msg':'Salvo com sucesso'}), 200


@app.route("/usuarios/<int:id>", methods = ["GET"])
def get_usuarios(id):
    db = Sessionlocal()
    usuario = db.query(Usuario).get(id)
    if (usuario):
        return jsonify(usuario.to_dict()), 200
    else:
        return jsonify({'msg':'Usuário não encontrado'}), 404

@app.route("/usuarios/delete/<int:id>", methods = ["GET"]) # antes não tinha delete e era DELETE
def delete_usuarios(id):
    db = Sessionlocal()
    usuario = db.query(Usuario).get(id)
    if (usuario):
        db.delete(usuario)
        db.commit()
        return redirect(url_for('novo', msg="Apagado com sucesso!"))
        #return jsonify({'msg':'Usuario apagado'}), 204
    else:
        return redirect(url_for('novo', msg="Dado não encontrado!"))


@app.route("/usuarios", methods = ["POST"])
def create_usuarios():
    db = Sessionlocal()
    data = request.get_json()
    usuario = Usuario(nome = data['nome'], data = data['aniversario'])
    db.add(usuario)
    db.commit()

    return jsonify({'msg':'Usuario criado com sucesso!', 'usu':usuario.to_dict()}), 201

@app.route("/usuarios/<int:id>", methods = ["PUT"])
def update_usuarios(id):
    db = Sessionlocal()
    ub = db.query(Usuario).get(id)
    data = request.get_json()
    ub.nome = data['nome']
    ub.data = data['aniversario']
    db.commit()

    return jsonify({'msg':'Usuario atualizado com sucesso!', 'usu':ub.to_dict()}), 200
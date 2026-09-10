import os
from flask import Flask, render_template, request, url_for, redirect, flash

from extensions import db
from sqlalchemy.sql import func

import logging as log
from werkzeug.utils import secure_filename

from dao.nascente.createNascente import inserirNascente
from dao.nascente.readNascente import listarNascentes,listarNascentesValidas

from models.nascente import Nascente
from models.usuario import Usuario


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///C:/vs_code_projetos/POC_AguasParaViver/database/database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route("/")
def mainPage():
    listaNascentesValidas = []
    listaNascentesValidas = listarNascentes()

    log.info(f"{listaNascentesValidas}")

    return render_template(
        "nascentes.html",
        nascentes=listaNascentesValidas
    )

@app.route("/cadastrarNascente", methods=["GET","POST"])
def cadastrarNascente():
    if request.method == "POST":

        endereco = request.form["endereco"]
        latitude = request.form["latitude"]
        longitude = request.form["longitude"]
        imagem = request.files["imagem"]
        descricao = request.form["descricao"]
        status = "PENDENTE"

        nomeImagem = secure_filename(imagem.filename)
        caminhoImagem = os.path.join("uploads", nomeImagem)
        imagem.save(os.path.join(app.static_folder, caminhoImagem))

        log.info(f"{nomeImagem}")
        log.info(f"{caminhoImagem}")

        nascente = Nascente(endereco,latitude,longitude,nomeImagem,descricao,status)

        log.info(f"{inserirNascente(nascente)}")
        flash("Nscente cadastrada com sucesso!", "success")

        return redirect("/")


    return render_template("cadastrarNascente.html")

if __name__ == "__main__":

    app.secret_key = "super secret key"

    with app.app_context():
        db.create_all()

    app.run(debug=True)

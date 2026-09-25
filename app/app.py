import os
import json
from flask import Flask, render_template, request, url_for, redirect, flash, session

from extensions import db
from sqlalchemy.sql import func

import logging as log
from werkzeug.utils import secure_filename

from dao.nascente.createNascente import inserirNascente
from dao.nascente.updateNascente import atualizarNascente
from dao.nascente.readNascente import listarNascentes,listarNascentesValidas, listarNascentesPendentes, buscarNascentePorId

from dao.usuario.createUsuario import inserirUsuario

from dao.visitaNascente.createVisita import criarVisita
from dao.visitaNascente.readVisita import listarVisitasNascente

from models.nascente import Nascente
from models.usuario import Usuario
from models.visitaNascente import VisitaNascente


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ('sqlite:///' + os.path.join(basedir, 'database.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


#Rotas de login, logout e cadastro de usuario

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        senha = request.form["password"]
        tipoUsuario = request.form["tipoUsuario"]

        usuario = Usuario.query.filter_by(
            email=email,
            tipoUsuario=tipoUsuario
        ).first()

        if usuario and usuario.senha == senha:

            session["usuario"] = usuario.nomeUsuario
            session["tipoUsuario"] = usuario.tipoUsuario

            return redirect("/")

        flash("Usuário não encontrado.", "error")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        nomeUsuario = request.form["nomeUsuario"]
        email = request.form["email"]
        senha = request.form["senha"]

        usuarioExistente = Usuario.query.filter_by(email=email).first()

        if usuarioExistente:
            flash("E-mail já cadastrado.", "error")
            return redirect("/register")

        usuario = Usuario(nomeUsuario=nomeUsuario, senha=senha, email=email, tipoUsuario="MEMBRO")

        resultado = inserirUsuario(usuario)

        if "erro" in resultado:
            flash("Erro ao realizar cadastro.", "error")
            return redirect("/register")

        flash("Cadastro realizado com sucesso!", "success")
        return redirect("/login")

    return render_template("register.html")



#rotas de Visualização e cadastro de mapas

@app.route("/")
def mainPage():
    listaNascentesValidas = []
    listaNascentesValidas = listarNascentes()

    log.info(f"{listaNascentesValidas}")

    return render_template(
        "nascentes.html",
        nascentes=listaNascentesValidas
    )

@app.route("/mapa")
def mapa():

    nascentes = listarNascentes()

    nascentesMapa = [
        {
            "id": nascente.id,
            "endereco": nascente.endereco,
            "latitude": nascente.latitude,
            "longitude": nascente.longitude,
            "descricao": nascente.descricao,
            "imagem": url_for("static", filename="uploads/" + nascente.imagem),
            "status": nascente.status,
        }
        for nascente in nascentes
    ]

    nascentesJSON = json.dumps(nascentesMapa).replace("<", "\\u003c")

    return render_template("mapa.html", nascentesJSON=nascentesJSON)

@app.route("/mapa/registrar", methods=["GET","POST"])
def cadastrarNascente():

    if not session.get("usuario"):
        return redirect("/login")
    
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


#Rota de redirecionamento edita ou historico nascente

@app.route("/dashboard/nascentes/<int:id>")
def detalhesNascente(id):

    nascente = buscarNascentePorId(id)

    return render_template("detalhesNascente.html",nascente=nascente)


#Rotas de Visualização e edição de nascentes

@app.route("/dashboard/nascentes")
def dashboardNascentes():

    nascentesPendentes = listarNascentesPendentes()
    nascentesAprovadas = listarNascentesValidas()

    return render_template("dashboardNascentes.html", nascentesPendentes=nascentesPendentes, nascentesAprovadas=nascentesAprovadas)

@app.route("/dashboard/nascentes/<int:id>/editar", methods=["GET", "POST"])
def editarNascente(id):

    nascente = Nascente.query.get(id)

    if not nascente:
        flash("Nascente não encontrada.", "error")
        return redirect("/dashboard/nascentes")

    if request.method == "POST":

        descricao = request.form["descricao"]
        acao = request.form["acao"]

        imagem = request.files.get("imagem")

        nomeImagem = None

        if imagem and imagem.filename:

            nomeImagem = secure_filename(imagem.filename)
            caminhoImagem = os.path.join("uploads",nomeImagem)

            imagem.save(os.path.join(app.static_folder, caminhoImagem))


        if acao == "validar":
            status = "APROVADA"
        elif acao == "invalidar":
            status = "DESAPROVADA"
        else:
            status = nascente.status

        resultado = atualizarNascente(
            id,
            nomeImagem,
            descricao,
            status
        )


        if "erro" in resultado:
            flash("Erro ao atualizar nascente.", "error")

            return redirect(f"/dashboard/nascentes/{id}/editar")


        visita = VisitaNascente(idNascente=id,imagem=nomeImagem if nomeImagem else nascente.imagem,descricao=descricao)

        log.info(criarVisita(visita))
        flash("Visita registrada com sucesso", "success")

        return redirect("/dashboard/nascentes")


    return render_template("editarNascente.html", nascente=nascente)

#Rota de visualização do historico de uma anscente

@app.route("/dashboard/nascentes/<int:id>/historico")
def historicoNascente(id):

    visitas = listarVisitasNascente(id)

    nascente = buscarNascentePorId(id)

    return render_template("historicoVisitas.html",nascente=nascente,visitas=visitas)

if __name__ == "__main__":

    app.secret_key = "super secret key"

    with app.app_context():
        db.create_all()

    app.run(debug=True)
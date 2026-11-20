from app import app
from extensions import db
from models.usuario import Usuario

from werkzeug.security import generate_password_hash

with app.app_context():

    email = "admin@teste.com"
    senha_hash = generate_password_hash("1234")

    usuario = Usuario.query.filter_by(email=email).first()

    if usuario:
        usuario.nomeUsuario = "Admin Teste"
        usuario.senha = senha_hash
        usuario.tipoUsuario = "ADMINISTRADOR"

        print("Administrador atualizado!")

    else:
        usuario = Usuario(
            "Admin Teste",
            senha_hash,
            email,
            "ADMINISTRADOR"
        )

        db.session.add(usuario)

        print("Administrador criado!")

    db.session.commit()

    print("bao")
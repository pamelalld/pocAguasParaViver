from app import app
from extensions import db
from models.usuario import Usuario

with app.app_context():
    usuario = Usuario(
        "Admin Teste",
        "1234",
        "admin@teste.com",
        "ADMINISTRADOR"
    )

    db.session.add(usuario)
    db.session.commit()

    print("bao")
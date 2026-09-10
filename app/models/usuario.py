from extensions import db

class Usuario(db.Model):
    __tablename__ = "usuario"

    id = db.Column(db.Integer, primary_key=True)
    nomeUsuario = db.Column(db.String(100), nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    tipoUsuario = db.Column(db.String(20), nullable=False)

    def __init__(self, nomeUsuario, senha, email, tipoUsuario):
        self.nomeUsuario = nomeUsuario
        self.senha = senha
        self.email = email
        self.tipoUsuario = tipoUsuario
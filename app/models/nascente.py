from extensions import db

class Nascente(db.Model):
    __tablename__ = "nascente"

    id = db.Column(db.Integer, primary_key=True)
    endereco = db.Column(db.String(255), nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    dataRegistro = db.Column(db.DateTime, nullable=False, default=db.func.now())
    imagem = db.Column(db.String(255), nullable=False)
    # dataAlteracao = db.Column(db.DateTime, nullable=True, onupdate=db.func.now())
    descricao = db.Column(db.Text, nullable=True)
    status = db.Column(db.Text, nullable=False)

    def __init__(self, endereco, latitude, longitude, imagem, descricao, status):
        self.endereco = endereco
        self.latitude = latitude
        self.longitude = longitude
        self.imagem = imagem
        self.descricao = descricao
        self.status = status
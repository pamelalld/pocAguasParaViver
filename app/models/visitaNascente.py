from extensions import db

class VisitaNascente(db.Model):
    __tablename__ = "visitaNascente"

    id = db.Column(db.Integer, primary_key=True)

    idNascente = db.Column(db.Integer,db.ForeignKey("nascente.id"),nullable=False)

    dataVisita = db.Column(db.DateTime,nullable=False,default=db.func.now())

    imagem = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)

    nascente = db.relationship("Nascente",back_populates="visitas")

    def __init__(self, idNascente, imagem, descricao, dataVisita=None):
        self.idNascente = idNascente
        self.imagem = imagem
        self.descricao = descricao

        if dataVisita is not None:
            self.dataVisita = dataVisita
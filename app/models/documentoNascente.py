from extensions import db

class DocumentoNascente(db.Model):
    __tablename__ = "documentoNascente"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    caminho = db.Column(db.String(255), nullable=False)

    nascente_id = db.Column(db.Integer, db.ForeignKey("nascente.id"), nullable=False)

    nascente = db.relationship("Nascente",back_populates="documentos")
from extensions import db
from models.documentoNascente import DocumentoNascente

def criarDocumento(documento):
    try:
        db.session.add(documento)
        db.session.commit()

        return {
            "mensagem": "Documento cadastrado com sucesso.",
            "documento": documento
        }

    except Exception as e:
        db.session.rollback()
        return {
            "erro": str(e)
        }
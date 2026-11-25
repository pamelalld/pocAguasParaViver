from extensions import db
from models.documentoNascente import DocumentoNascente

def buscarDocumentosNascente(nascente_id):
    try:
        documentos = DocumentoNascente.query.filter_by(
            nascente_id=nascente_id
        ).all()

        return {
            "documentos": documentos
        }

    except Exception as e:
        return {
            "erro": str(e)
        }

def buscarDocumentoPorId(documento_id):
    try:
        documento = db.session.get(
            DocumentoNascente,
            documento_id
        )

        if documento is None:
            return {
                "erro": "Documento não encontrado."
            }

        return {
            "documento": documento
        }

    except Exception as e:
        return {
            "erro": str(e)
        }
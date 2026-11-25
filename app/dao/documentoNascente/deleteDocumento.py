from extensions import db
from models.documentoNascente import DocumentoNascente

def excluirDocumento(documento_id):
    try:
        documento = db.session.get(
            DocumentoNascente,
            documento_id
        )

        if documento is None:
            return {
                "erro": "Documento não encontrado."
            }

        db.session.delete(documento)
        db.session.commit()

        return {
            "mensagem": "Documento excluído com sucesso."
        }

    except Exception as e:
        db.session.rollback()
        return {
            "erro": str(e)
        }
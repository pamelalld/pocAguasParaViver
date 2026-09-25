from extensions import db
from models.visitaNascente import VisitaNascente

def criarVisita(visita):
    try:
        db.session.add(visita)
        db.session.commit()

        return {
            "mensagem": "Visita cadastrada com sucesso.",
            "visita": visita
        }

    except Exception as e:
        db.session.rollback()
        return {
            "erro": str(e)
        }
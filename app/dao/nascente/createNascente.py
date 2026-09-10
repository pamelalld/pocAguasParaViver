from extensions import db
from models.nascente import Nascente

def inserirNascente(nascente):
    try:
        db.session.add(nascente)
        db.session.commit()

        return {
            "mensagem": "Nascente inserida com sucesso",
            "id": nascente.id
        }

    except Exception as e:
        db.session.rollback()
        return {"erro": str(e)}
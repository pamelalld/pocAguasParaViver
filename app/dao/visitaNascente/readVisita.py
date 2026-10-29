from extensions import db
from models.visitaNascente import VisitaNascente

def listarVisitasNascente(idNascente):
    try:
        visitas = (
            VisitaNascente.query
            .filter_by(idNascente=idNascente)
            .order_by(VisitaNascente.dataVisita.desc())
            .all()
        )

        return visitas

    except Exception as e:
        return {
            "erro": str(e)
        }
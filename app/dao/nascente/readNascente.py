from extensions import db
from models.nascente import Nascente

def listarNascentes():
    try:
        nascentes = Nascente.query.all()

        return nascentes

    except Exception as e:
        return {"erro": str(e)}

def listarNascentesValidas():
    try:
        nascentes = Nascente.query.filter_by(status="VALIDO").all()

        return nascentes

    except Exception as e:
        return {"erro": str(e)}

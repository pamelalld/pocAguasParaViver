from extensions import db
from models.nascente import Nascente

def atualizarNascente(id, imagem=None, descricao=None, status=None, endereco=None, latitude=None, longitude=None):
    try:
        nascente = Nascente.query.get(id)

        if not nascente:
            return {"erro": "Nascente não encontrada"}

        if imagem:
            nascente.imagem = imagem

        if descricao is not None:
            nascente.descricao = descricao

        if status is not None:
            nascente.status = status

        if endereco is not None:
            nascente.endereco = endereco

        if latitude is not None:
            nascente.latitude = latitude

        if longitude is not None:
            nascente.longitude = longitude

        db.session.commit()

        return {
            "mensagem": "Nascente atualizada com sucesso"
        }

    except Exception as e:
        db.session.rollback()
        return {"erro": str(e)}
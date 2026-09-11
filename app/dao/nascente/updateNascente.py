from extensions import db
from models.nascente import Nascente

def atualizarNascente(id, imagem=None, descricao=None, status=None):
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

        db.session.commit()

        return {
            "mensagem": "Nascente atualizada com sucesso"
        }

    except Exception as e:
        db.session.rollback()
        return {"erro": str(e)}
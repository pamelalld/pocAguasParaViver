from extensions import db
from models.usuario import Usuario

def inserirUsuario(usuario):
    try:
        db.session.add(usuario)
        db.session.commit()

        return {
            "mensagem": "Usuário inserido com sucesso",
            "id": usuario.id
        }

    except Exception as e:
        db.session.rollback()
        return {"erro": str(e)}
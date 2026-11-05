from extensions import db
from models.usuario import Usuario


USUARIOS_PADRAO = (
    {
        "nomeUsuario": "Administrador",
        "email": "admin@aguasparaviver.com",
        "senha": "admin123",
        "tipoUsuario": "ADMINISTRADOR",
    },
    {
        "nomeUsuario": "Membro Comum",
        "email": "membro@aguasparaviver.com",
        "senha": "membro123",
        "tipoUsuario": "MEMBRO",
    },
)


def criarUsuariosPadrao():
    criados = []

    for dados in USUARIOS_PADRAO:
        if Usuario.query.filter_by(email=dados["email"]).first():
            continue

        usuario = Usuario(
            dados["nomeUsuario"],
            dados["senha"],
            dados["email"],
            dados["tipoUsuario"],
        )

        db.session.add(usuario)
        criados.append(dados["email"])

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        raise

    return criados


if __name__ == "__main__":
    from app import app

    with app.app_context():
        db.create_all()

        criados = criarUsuariosPadrao()

        if criados:
            print("Usuários criados:", ", ".join(criados))
        else:
            print("Usuários padrão já existem.")

from extensions import db
from models.usuario import Usuario
from werkzeug.security import generate_password_hash


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
    atualizados = []


    for dados in USUARIOS_PADRAO:
        usuario = Usuario.query.filter_by(email=dados["email"]).first()

        senhaHash = generate_password_hash(dados["senha"])

        if usuario:
            usuario.nomeUsuario = dados["nomeUsuario"]
            usuario.senha = senhaHash
            usuario.tipoUsuario = dados["tipoUsuario"]

            atualizados.append(dados["email"])

        else:
            usuario = Usuario(
                dados["nomeUsuario"],
                senhaHash,
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

    return criados, atualizados


if __name__ == "__main__":
    from app import app

    with app.app_context():
        db.create_all()

        criados = criarUsuariosPadrao()

        if criados:
            print("Usuários criados:", ", ".join(criados))
        else:
            print("Usuários padrão já existem.")

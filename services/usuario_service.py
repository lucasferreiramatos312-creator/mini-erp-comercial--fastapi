from repositories.usuario_repository import criar_usuario, buscar_usuario_por_email
from security.security import gerar_hash, verificar_senha


def registrar_usuario(nome, email, senha):

    senha_hash = gerar_hash(senha)

    criar_usuario(nome, email, senha_hash)


def autenticar_usuario(email, senha):

    usuario = buscar_usuario_por_email(email)

    if not usuario:
        return None

    senha_valida = verificar_senha(senha, usuario.Senha)

    if not senha_valida:
        return None

    return usuario
from repositories.usuario_repository import criar_usuario, buscar_usuario_por_email
from security.auth import gerar_hash, verificar_senha
from exceptions.custom_exceptions import AutenticacaoException,ValidacaoException


def registrar_usuario(nome, email, senha):

    usuario = buscar_usuario_por_email(email)

    if usuario:
        raise ValidacaoException("Email já cadastrado")

    senha_hash = gerar_hash(senha)

    criar_usuario(nome, email, senha_hash)


def autenticar_usuario(email, senha):

    usuario = buscar_usuario_por_email(email)

    if not usuario:
        raise AutenticacaoException("Email ou senha inválidos")

    senha_valida = verificar_senha(senha, usuario.Senha)

    if not senha_valida:
        raise AutenticacaoException("Email ou senha inválidos")

    return usuario
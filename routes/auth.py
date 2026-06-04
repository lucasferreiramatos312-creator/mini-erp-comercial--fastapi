from fastapi import APIRouter, HTTPException
from models.usuario_model import UsuarioCreate, UsuarioLogin
from services.usuario_service import registrar_usuario, autenticar_usuario
from security.auth import criar_token
from utils.responses import sucesso
from utils.logger import logger

router = APIRouter()

@router.post("/auth/registrar")
def registrar(usuario: UsuarioCreate):

    registrar_usuario(
        usuario.nome,
        usuario.email,
        usuario.senha
    )

    logger.info(f"Novo usuário cadastrado | email={usuario.email}")

    return sucesso(mensagem="Usuário criado com sucesso")


@router.post("/auth/login")
def login(usuario: UsuarioLogin):

    user = autenticar_usuario(
        usuario.email,
        usuario.senha
    )

    logger.info(f"Login realizado | email={usuario.email}")
    
    token = criar_token({
        "id": user[0],
        "email": user[2]
    })

    return sucesso(
        dados={
        "access_token": token,
        "token_type": "bearer"
        },
        mensagem="Login realizado com sucesso"
    )
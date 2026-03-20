from fastapi import APIRouter, HTTPException
from models.usuario_model import UsuarioCreate, UsuarioLogin
from services.usuario_service import registrar_usuario, autenticar_usuario
from security.security import criar_token

router = APIRouter()

@router.post("/auth/registrar")
def registrar(usuario: UsuarioCreate):

    registrar_usuario(
        usuario.nome,
        usuario.email,
        usuario.senha
    )

    return {"mensagem": "Usuário criado com sucesso"}


@router.post("/auth/login")
def login(usuario: UsuarioLogin):

    user = autenticar_usuario(
        usuario.email,
        usuario.senha
    )

    if not user:
        raise HTTPException(status_code=401, detail="Email ou senha inválidos")

    token = criar_token({
        "id": user.Id,
        "email": user.Email
    })

    return {
        "access_token": token,
        "token_type": "bearer"
    }
from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta, UTC
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends
from exceptions.custom_exceptions import AutenticacaoException

from dotenv import load_dotenv
import os

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def gerar_hash(senha: str):
    return pwd_context.hash(senha)

def verificar_senha(senha_digitada: str, hash_salvo: str):
    return pwd_context.verify(senha_digitada, hash_salvo)

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
TEMPO_EXPIRACAO = int(os.getenv("TEMPO_EXPIRACAO"))

def criar_token(dados: dict):

    dados_token = dados.copy()

    expira = datetime.now(UTC) + timedelta(minutes=TEMPO_EXPIRACAO)

    dados_token.update({"exp": expira})

    token = jwt.encode(dados_token, SECRET_KEY, algorithm=ALGORITHM)

    return token

security = HTTPBearer()

def verificar_token(credentials: HTTPAuthorizationCredentials):

    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return payload

    except JWTError:

        raise AutenticacaoException("Token inválido ou expirado")
    
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    
    payload = verificar_token(credentials)

    usuario_id = payload.get("id")

    if not usuario_id:
        raise AutenticacaoException("Usuário inválido")

    return usuario_id
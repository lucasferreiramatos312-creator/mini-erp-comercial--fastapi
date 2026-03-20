from passlib.context import CryptContext
from jose import jwt, JWTError
from datetime import datetime, timedelta
from fastapi import HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def gerar_hash(senha: str):
    return pwd_context.hash(senha)

def verificar_senha(senha_digitada: str, hash_salvo: str):
    return pwd_context.verify(senha_digitada, hash_salvo)


SECRET_KEY = "chave_super_secreta_do_sistema"
ALGORITHM = "HS256"
TEMPO_EXPIRACAO = 60

def criar_token(dados: dict):

    dados_token = dados.copy()

    expira = datetime.utcnow() + timedelta(minutes=TEMPO_EXPIRACAO)

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

        raise HTTPException(
            status_code=401,
            detail="Token inválido ou expirado"
        )
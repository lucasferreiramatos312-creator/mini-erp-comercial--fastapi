from pydantic import BaseModel
from datetime import datetime

class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str

class UsuarioLogin(BaseModel):
    email: str
    senha: str

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    data_cadastro: datetime
from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str
    
    @field_validator('nome')
    def validar_nome(cls, v):
        
        if not v.strip():
            raise ValueError("Nome obrigatório")
        
        return v
    
    @field_validator('senha')
    def validar_senha(cls, v):
        
        if not v.strip():
            raise ValueError("Senha não pode estar vazia")
        
        return v

class UsuarioLogin(BaseModel):
    email: str
    senha: str

class UsuarioResponse(BaseModel):
    id: int
    nome: str
    email: str
    data_cadastro: datetime
from pydantic import BaseModel, EmailStr, field_validator

class ClienteCreate(BaseModel):
    nome: str
    email: EmailStr
    telefone: str

    @field_validator('nome')
    def validar_nome(cls, v):
        
        if not v.strip():
            raise ValueError("Nome obrigatório")
        
        return v

    @field_validator('telefone')
    def validar_telefone(cls, v):
        v = v.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")

        if not v.isdigit():
            raise ValueError('O telefone deve conter apenas números.')
        
        if len(v) < 10 or len(v) > 11:
            raise ValueError("Telefone inválido")
        return v
                         
class ClienteResponse(BaseModel):
    id: int
    nome: str
    email: str
    telefone: str
    ativo: int
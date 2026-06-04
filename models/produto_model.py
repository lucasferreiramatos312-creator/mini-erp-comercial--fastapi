from pydantic import BaseModel, field_validator

class Produto(BaseModel):
    nome: str
    valor: float
    estoque: int

    @field_validator('nome')
    def validar_nome(cls, v):
        
        if not v.strip():
            raise ValueError("Nome obrigatório")
        
        return v
    
    @field_validator('valor')
    def validar_valor(cls, v):

        if v <= 0:
            raise ValueError("Valor deve ser maior que zero")
        
        return v
    
    @field_validator('estoque')
    def validar_estoque(cls, v):
        
        if v < 0:
            raise ValueError("Estoque inválido")
        
        return v
    
class ProdutoResponse(BaseModel):
    id: int
    nome: str
    valor: float
    estoque: int
    ativo: int
from pydantic import BaseModel, Field

class Produto(BaseModel):
    nome_produto: str
    valor: float = Field(gt=0)
    

class ProdutoResponse(BaseModel):
    id: int
    usuario: str
    produto: str
    valor: float 
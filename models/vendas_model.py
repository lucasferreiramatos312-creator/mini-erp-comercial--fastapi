from pydantic import BaseModel, field_validator
from typing import List

class ItemmVendaCreate(BaseModel):
    produto_id: int
    quantidade: int
    
    @field_validator('quantidade')
    def validar_quatidade(cls, v):

        if v <= 0:
            raise ValueError("Quantidade deve ser maior que zero")
        
        return v

class VendaCreate(BaseModel):
    cliente_id: int
    itens: List[ItemmVendaCreate]

class ItemVendaResponse(BaseModel):
    produto_id: int
    produto_nome: str
    quantidade: int
    valor_unitario: float

class VendaResponse(BaseModel):
    id: int
    cliente_id: int
    cliente_nome: str
    data_venda: str
    total: float
    status : str
    total_pago : float
    itens: List[ItemVendaResponse]

class AtualiarQuantidadeItem(BaseModel):
    quantidade: int

    @field_validator("quantidade")
    def validar_quantidade(cls, v):
        if v <=0:
            raise ValueError("Quantidade deve ser maior que zero")

        return v

class PagamentoCreate(BaseModel):
    valor_pago: float

    @field_validator('valor_pago')
    def validar_valor_pagp(cls, v ):

        if v <= 0:
            raise ValueError("O valor pago deve ser maior que zero")

        return v
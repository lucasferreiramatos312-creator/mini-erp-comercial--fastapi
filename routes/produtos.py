from fastapi import APIRouter, HTTPException, status
from models.produto_model import Produto, ProdutoResponse
from fastapi import Depends
from security.security import verificar_token, security
from services.produto_service import (
    listar as listar_service,
    buscar as buscar_service,
    criar as criar_service,
    atualizar as atualizar_service,
    deletar as deletar_service
)

router = APIRouter(prefix="/api/produtos", tags=["Produtos"])


@router.get("", response_model=list[ProdutoResponse])
def listar(token = Depends(security)):

    payload = verificar_token(token)

    id_usuario = payload.get("id")

    produtos = listar_service(id_usuario)

    resultado = [
        {
            "id": linha[0],
            "usuario": linha[1],
            "produto": linha[2],
            "valor": float(linha[3])
        }
        for linha in produtos
    ]

    return resultado


@router.get("/{id}", response_model=ProdutoResponse)
def buscar(id: int, token = Depends(security)):

    payload = verificar_token(token)
    id_usuario = payload.get("id")

    produto = buscar_service(id)

    if not produto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    
    if produto[4] != id_usuario:
        raise HTTPException(status_code=403,detail="Acesso negado")

    return {
        "id": produto[0],
        "usuario": produto[1],
        "produto": produto[2],
        "valor": float(produto[3])
    }


@router.post("", status_code=status.HTTP_201_CREATED)
def criar(produto: Produto, token = Depends(security)):

    payload = verificar_token(token)
    id_usuario = payload.get("id")

    criar_service(
        produto.nome_produto,
        produto.valor,
        id_usuario
    )

    return {"mensagem": "Produto criado com sucesso"}


@router.put("/{id}")
def atualizar(id: int, produto: Produto, token = Depends(security)):

    payload = verificar_token(token)
    id_usuario = payload.get("id")

    produto_existente = buscar_service(id)

    if not produto_existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    
    if produto_existente[4] != id_usuario:
        raise HTTPException(STATUS_CODE=403, detail="Acesso negado")

    atualizar_service(
        id,
        produto.nome_produto,
        produto.valor,
        id_usuario
    )

    return {"mensagem": "Produto atualizado"}


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def deletar(id: int, token = Depends(security)):

    payload = verificar_token(token)
    id_usuario = payload.get("id")

    produto_existente = buscar_service(id)

    if not produto_existente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Produto não encontrado"
        )
    
    if produto_existente[4] != id_usuario:
        raise HTTPException(status_code=403, detail="Acesso negado")

    deletar_service(id)

    return {"mensagem": "Produto deletado"}
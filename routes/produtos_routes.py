from fastapi import APIRouter, Depends
from models.produto_model import Produto, ProdutoResponse
from utils.responses import sucesso
from utils.logger import logger
from security.auth import get_current_user
from services.produto_service import (
    listar_produto_service,
    buscar_produto_por_id_geral_service,
    buscar_produto_por_nome_service,
    criar_produto_service,
    atualizar_produto_service,
    listar_produtos_inativos_service,
    inativar_produto_service,
    reativar_produto_service
)

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.post("/")
def criar(produto: Produto, usuario=Depends(get_current_user)):

    novo_produto = criar_produto_service(produto.nome, produto.valor, produto.estoque, usuario)
    
    logger.info(f"Novo produto criado | produto={produto.nome} | usuario={usuario}")

    return sucesso(dados=novo_produto, mensagem="Produto criado com sucesso")

@router.get("/inativos")
def listar_produtos_inativos(usuario=Depends(get_current_user)):

    produtos = listar_produtos_inativos_service(usuario)

    return sucesso(dados=produtos, mensagem="Produtos inativos encontrados")

@router.get("/")
def listar_ou_buscar(nome: str = None, usuario=Depends(get_current_user)):
    
    if nome:
        return sucesso(dados=buscar_produto_por_nome_service(nome, usuario), mensagem="Produto encontrado")
    
    return sucesso(dados=listar_produto_service(usuario), mensagem="Produtos encontrados")

@router.get("/{id}")
def buscar_produto_por_id_geral(id: int, usuario=Depends(get_current_user)):

    produto = buscar_produto_por_id_geral_service(id, usuario)

    return sucesso(dados=produto, mensagem="Produto encontrado")

@router.put("/{id}/reativar")
def reativar_produto(id: int, usuario=Depends(get_current_user)):
     
    produto = reativar_produto_service(id, usuario)

    logger.info(f"Produto reativado | produto={id} | usuario={usuario}")

    return sucesso(dados=produto, mensagem="Produto reativado com sucesso")

@router.put("/{id}")
def atualizar(id: int, produto: Produto, usuario=Depends(get_current_user)):
    
    produto_atualizado = atualizar_produto_service(
        id,
        produto.nome,
        produto.valor,
        produto.estoque,
        usuario
    )
    
    logger.info(f"Produto atualizado | produto={id} | usuario={usuario}")

    return sucesso(dados=produto_atualizado, mensagem="Produto atualizado")

@router.put("/{id}/inativar")
def inativar(id: int, usuario=Depends(get_current_user)):
            
    produto = inativar_produto_service(id, usuario)
    
    logger.info(f"Produto inativado | produto={id} | usuario={usuario}")

    return sucesso(dados=produto, mensagem="Produto inativado com sucesso")
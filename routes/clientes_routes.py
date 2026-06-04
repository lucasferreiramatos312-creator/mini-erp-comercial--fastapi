from fastapi import APIRouter, Depends

from models.cliente_model import ClienteCreate

from security.auth import get_current_user

from utils.responses import sucesso
from utils.logger import logger

from services.clientes_service import (criar_cliente_service,
                                       listar_clientes_service,
                                       buscar_cliente_por_nome_service,
                                       buscar_cliente_por_id_geral_service,
                                       atualizar_cliente_service,
                                       listar_clientes_inativos_service,
                                       inativar_cliente_service,
                                       reativar_cliente_service)

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/")
def criar_cliente(cliente: ClienteCreate, usuario=Depends(get_current_user)):
    
    novo_cliente = criar_cliente_service(cliente.nome, cliente.email, cliente.telefone, usuario)
    
    logger.info(f"Novo cliente cadastrado | clinte={cliente.nome} | usuario={usuario}")
    
    return sucesso(dados=novo_cliente, mensagem="Cliente criado com sucesso")

@router.get("/inativos")
def listar_clientes_inativos(usuario=Depends(get_current_user)):

   clientes =  listar_clientes_inativos_service(usuario)

   return sucesso(dados=clientes, mensagem="Clientes inativos encontrados")

@router.get("/")
def listar_ou_buscar_clientes(nome: str = None, usuario=Depends(get_current_user)):
    
    if nome:
        return sucesso(dados=buscar_cliente_por_nome_service(nome, usuario), mensagem="Clientes encontrados")
    
    return sucesso(dados=listar_clientes_service(usuario), mensagem="Clientes encontrados")

@router.get("/{id}")
def buscar_cliente_por_id_geral(id: int, usuario=Depends(get_current_user)):

    cliente = buscar_cliente_por_id_geral_service(id, usuario)

    return sucesso(dados=cliente, mensagem="Cliente encontrado")

@router.put("/{id}")
def atualizar_cliente(id: int, cliente: ClienteCreate, usuario=Depends(get_current_user)):

    cliente_atualizado = atualizar_cliente_service(
        id,
        cliente.nome,
        cliente.email,
        cliente.telefone,
        usuario
    )

    logger.info(f"Cliente atualizado | cliente={id} | usuario={usuario}")

    return sucesso(dados=cliente_atualizado, mensagem="Cliente atualizado")

@router.put("/{id}/reativar")
def reativar_cliente(id: int, usuario=Depends(get_current_user)):

    cliente = reativar_cliente_service(id, usuario)

    logger.info(f"Cliente reativado | cliente={id} | usuario={usuario}")

    return sucesso(dados=cliente, mensagem="Cliente reativado com sucesso")

@router.put("/{id}/inativar")
def inativar_cliente(id: int, usuario=Depends(get_current_user)):
    
    cliente = inativar_cliente_service(id, usuario)
    
    logger.info(f"Cliente inativado | cliente={id} | usuario={usuario}")
    
    return sucesso(dados=cliente, mensagem="Cliente inativado com sucesso")
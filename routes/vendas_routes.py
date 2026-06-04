from fastapi import APIRouter, Depends
from security.auth import get_current_user
from models.vendas_model import PagamentoCreate, VendaCreate, ItemmVendaCreate, AtualiarQuantidadeItem
from utils.responses import sucesso
from utils.logger import logger
from services.vendas_service import (criar_venda_service,
                                    adicionar_item_service,
                                    criar_venda_com_itens,
                                    listar_vendas_service,
                                    listar_vendas_fechadas_service,
                                    buscar_venda_com_itens_service,
                                    buscar_venda_por_cliente_service,
                                    atualizar_item_venda_service,
                                    excluir_venda_service,
                                    fechar_vendas_pagadas_service,
                                    registrar_pagamento_service)

router = APIRouter(prefix="/vendas", tags=["Vendas"])

@router.post("/")
def criar_venda(venda:VendaCreate, usuario=Depends(get_current_user)):

    venda = criar_venda_com_itens(venda, usuario)
        
    logger.info(f"venda criada | venda={venda['id']} | usuario={usuario}")
        
    return sucesso(dados=venda, mensagem="Venda criada com sucesso")
    
@router.post("/simples")
def criar_venda_simples(venda:VendaCreate, usuario=Depends(get_current_user)):

    venda = criar_venda_service(venda.cliente_id, usuario)

    logger.info(f"Venda criada com sucesso venda={venda['id']} | usuario={usuario}")
        
    return sucesso(dados=venda, mensagem="Venda criada (sem itens)")
    
@router.post("/{venda_id}/itens")
def adicionar_item(venda_id: int, item: ItemmVendaCreate, usuario=Depends(get_current_user)):
        
    adicionar_item_service(venda_id, item.produto_id, item.quantidade, usuario)

    venda = buscar_venda_com_itens_service(venda_id, usuario)
        
    logger.info(f"Item adicionado | venda={venda_id} | produto={item.produto_id} | usuario={usuario}")
        
    return sucesso(dados=venda, mensagem="Item adicionado com sucesso")
    
@router.get("/",)
def listar_ou_buscar(nome: str = None, mes: int = None, ano: int = None, usuario=Depends(get_current_user)):
    
    if nome and nome.strip():
        venda = buscar_venda_por_cliente_service(nome, usuario)
        return sucesso(dados=venda,mensagem="Vendas encontradas")
    
    vendas = listar_vendas_service(usuario, mes, ano)
    return sucesso(dados=vendas,mensagem="Vendas listadas com sucesso")

@router.get("/historico")
def listar_historico_vendas(mes: int = None, ano: int = None, usuario=Depends(get_current_user)):
        
    return sucesso(dados=listar_vendas_fechadas_service(usuario, mes, ano), mensagem="Vendas listadas com sucesso")

@router.get("/{venda_id}")
def buscar_venda(venda_id: int, usuario=Depends(get_current_user)):

    logger.info(f"Historico de vendas consultado | usuario={usuario}")
    
    venda = buscar_venda_com_itens_service(venda_id, usuario)

    return sucesso(dados=venda, mensagem="Venda encontrada")
    
@router.put("/{venda_id}/itens/{produto_id}")
def atualizar_item(venda_id: int, produto_id: int, item: AtualiarQuantidadeItem, usuario=Depends(get_current_user)):

    atualizar_item_venda_service(venda_id, produto_id, item.quantidade, usuario)

    venda = buscar_venda_com_itens_service(venda_id, usuario)

    logger.info(f"Item atualizado | venda={venda_id} | produto={produto_id} | usuario={usuario}")

    return sucesso(dados=venda, mensagem="Item atualizado com sucesso")
        
@router.delete("/{venda_id}")
def excluir_venda(venda_id: int, usuario=Depends(get_current_user)):

        excluir_venda_service(venda_id, usuario)
        
        logger.info(f"Venda deletada | venda={venda_id} | usuario={usuario}")

        return sucesso(mensagem="Venda excluída com sucesso")
 
@router.post("/{venda_id}/pagamentos")
def pagar(venda_id: int, pagamento: PagamentoCreate, usuario=Depends(get_current_user)):

    registrar_pagamento_service(venda_id,
                                    pagamento.valor_pago,
                                    usuario)
    
    venda = buscar_venda_com_itens_service(venda_id, usuario)
        
    logger.info(f"Pagamento efetuado | venda={venda_id} | usuario={usuario}")

    return sucesso(dados=venda, mensagem="Pagamento registrado")

@router.post("/fechar-mes")
def fechar_mes(usuario=Depends(get_current_user)):
        
        vendas = fechar_vendas_pagadas_service(usuario)

        logger.info(f"Fechamento feito com sucesso | usuario={usuario}")
        
        return sucesso(dados=vendas, mensagem="Vendas pagas do mês fechadas")
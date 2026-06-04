from repositories.produtos_repository import (
    listar_produtos,
    buscar_produto_por_id_geral,
    buscar_produto_por_id,
    buscar_produto_por_nome,
    criar_produto,
    atualizar_produto,
    listar_produtos_inativos,
    inativar_produto,
    reativar_produto
)
from exceptions.custom_exceptions import ProdutoNaoEncontrado

def formatar_produto(produto):

    return {
        "id": produto[0],
        "nome": produto[1],
        "valor": produto[2],
        "estoque": produto[3],
        "ativo": produto[4]
    }


def criar_produto_service(nome, valor, estoque, usuario_id):
    
    produto_id = criar_produto(nome, valor, estoque, usuario_id)

    novo_produto = buscar_produto_por_id_geral(produto_id,usuario_id)

    return formatar_produto(novo_produto)

def listar_produto_service(usuario_id):

    produtos =  listar_produtos(usuario_id)

    return [formatar_produto(p) for p in produtos]

def buscar_produto_por_id_geral_service(id,usuario_id):

    produto = buscar_produto_por_id_geral(id, usuario_id)

    return formatar_produto(produto)
    
def buscar_produto_por_nome_service(nome,usuario_id):
    
    produtos = buscar_produto_por_nome(nome, usuario_id)

    if not produtos:
        raise ProdutoNaoEncontrado()
    
    return [formatar_produto(p) for p in produtos]

def atualizar_produto_service(id, nome, valor, estoque, usuario_id):

    produto_existente = buscar_produto_por_id(id, usuario_id)

    if not produto_existente:
        raise ProdutoNaoEncontrado()    

    atualizar_produto(id, nome, valor, estoque, usuario_id)

    produto_atualizado = buscar_produto_por_id(id,usuario_id)

    return formatar_produto(produto_atualizado)

def listar_produtos_inativos_service(usuario_id):

    produtos =  listar_produtos_inativos(usuario_id)

    return [formatar_produto(p) for p in produtos]

def inativar_produto_service(id, usuario_id):

    produto = buscar_produto_por_id(id, usuario_id)

    if not produto:
        raise ProdutoNaoEncontrado()
    
    produto_inativado = inativar_produto(id, usuario_id)

    return formatar_produto(produto_inativado)

def reativar_produto_service(id, usuario_id):

    produto = buscar_produto_por_id_geral(id, usuario_id)

    if not produto:
        raise ProdutoNaoEncontrado()
    
    produto_reativado = reativar_produto(id, usuario_id)
    
    return formatar_produto(produto_reativado)
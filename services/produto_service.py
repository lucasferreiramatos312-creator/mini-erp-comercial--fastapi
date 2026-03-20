from repositories.produto_repository import (
    listar_produtos,
    buscar_produto,
    criar_produto,
    atualizar_produto,
    deletar_produto
)


def listar(id_usuario: int):
    return listar_produtos(id_usuario)


def buscar(id):
    return buscar_produto(id)


def criar(nome_produto, valor, id_usuario):
    criar_produto(nome_produto, valor, id_usuario)


def atualizar(id, nome_produto, valor, id_usuario):
    atualizar_produto(id, nome_produto, valor, id_usuario)


def deletar(id):
    deletar_produto(id)
from tests.helpers.produtos import (
                                    criar_produto_com_nome_valor_estoque,
                                    buscar_produto_por_id,
                                    buscar_produto_por_nome,
                                    listar_produtos_ativos,
                                    atualizar_produto,
                                    inativar_produto,
                                    listar_produtos_inativos,
                                    reativar_produto
                                    )

def test_de_fluxo_completo_produtos(client, token):
    
    criar_produto = criar_produto_com_nome_valor_estoque(client, token,
                                                         nome="Aliança de Ouro Falso",
                                                         valor=10.50,
                                                         estoque=5
                                                         )
    
    criar_produto_invalido = criar_produto_com_nome_valor_estoque(client, token,
                                                                     nome="  ",
                                                                     valor=None,
                                                                     estoque=-1
                                                                    )
    
    assert criar_produto_invalido.status_code == 422
    
    assert criar_produto.status_code == 200

    novo_produto = criar_produto.json()["dados"]

    buscar_produto_nome = buscar_produto_por_nome(client, token, "Aliança de Ouro Falso")

    assert any(c["nome"] == "Aliança de Ouro Falso" for c in buscar_produto_nome)
    buscar_produto_id = buscar_produto_por_id(client, token, novo_produto["id"])

    assert buscar_produto_id["id"] == novo_produto["id"]

    produtos_ativos = listar_produtos_ativos(client, token)
    assert any(c["id"] == buscar_produto_id["id"] for c in produtos_ativos)

    produto_foi_atualizado = atualizar_produto(client, token,
                                          nome="Aliança de Ouro 18K",
                                          valor=2569.99,
                                          estoque=10
                                         )
    
    produto_atualizado_invalido = atualizar_produto(client, token,
                                                   nome=None,
                                                   valor="str",
                                                   estoque="str"
                                                    )
    
    assert produto_atualizado_invalido.status_code == 422

    assert produto_foi_atualizado.status_code == 200

    produto_atualizado = produto_foi_atualizado.json()["dados"]

    assert produto_atualizado["nome"] == "Aliança de Ouro 18K"
    assert produto_atualizado["valor"] == 2569.99
    assert produto_atualizado["estoque"] == 10

    produto_inativado = inativar_produto(client, token, produto_atualizado["id"])

    assert produto_inativado["ativo"] is False

    produtos_inativos = listar_produtos_inativos(client, token)
    assert any(c["id"] == produto_atualizado["id"] for c in produtos_inativos)

    produto_reativado = reativar_produto(client, token, produto_inativado["id"])

    assert produto_reativado["ativo"] is True
    produtos_ativos = listar_produtos_ativos(client, token)

    assert any(c["id"] == produto_reativado["id"] for c in produtos_ativos)
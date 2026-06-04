from tests.helpers.auth import criar_usuario, login_usuario

from tests.helpers.produtos import (
                                    criar_produto_com_nome_valor_estoque,
                                    buscar_produto_por_id,
                                    inativar_produto,
                                    reativar_produto
                                    )

from tests.helpers.clientes import (
                                    criar_cliente_com_nome_email_telefone,
                                    buscar_cliente_por_id,
                                    inativar_cliente,
                                    listar_clientes_inativos,
                                    reativar_cliente)


from tests.helpers.vendas import (
                                    criar_venda_simples_por_cliente_id,
                                    criar_item_e_adicionar_quantidade,
                                    buscar_venda_por_id,
                                    fazer_pagamento_venda,
                                    fechar_venda_mes,
                                    listar_vendas_fechadas,
                                    criar_venda_simples_erro,
                                    criar_item_e_adicionar_erro
                                    )

def test_completo_sistema(client, token):
    
    criar_usuario()

    token = login_usuario()

    produto1_criado = criar_produto_com_nome_valor_estoque(client, token,
                                                   nome="Produto X",
                                                   valor=100.0,
                                                   estoque=10)
    produto1_data = produto1_criado.json()["dados"]

    produto_X = buscar_produto_por_id(client, token, produto1_data["id"])
    assert produto_X["id"] == produto1_data["id"]
    assert produto_X["estoque"] == 10

    produto2_criado = criar_produto_com_nome_valor_estoque(client, token,
                                                   nome="Produto Y",
                                                   valor=100.0,
                                                   estoque=10)
    produto2_data = produto2_criado.json()["dados"]

    produto_Y = buscar_produto_por_id(client, token, produto2_data["id"])
    assert produto_Y["id"] == produto2_data["id"]
    assert produto_Y["estoque"] == 10

    cliente_criado = criar_cliente_com_nome_email_telefone(client, token,
                                                    nome="Cliente X",
                                                    email="clientex@email.com",
                                                    telefone="11999999999")
    
    cliente_data = cliente_criado.json()["dados"]

    cliente = buscar_cliente_por_id(client, token, cliente_data["id"])
    assert cliente["id"] == cliente_data["id"]

    venda1_criada = criar_venda_simples_por_cliente_id(client, token, cliente_id=cliente["id"])

    item1_adicionado = criar_item_e_adicionar_quantidade(client, token,
                                              venda1_criada["id"],
                                              produto_X["id"],
                                              quantidade=1)
    item2_adicionado = criar_item_e_adicionar_quantidade(client, token,
                                              venda1_criada["id"],
                                              produto_Y["id"],
                                              quantidade=2)

    venda_com_itens = buscar_venda_por_id(client, token, venda1_criada["id"])
    assert len(venda_com_itens["itens"]) == 2
    assert venda_com_itens["total"] == 300.0
    assert venda_com_itens["status"] == "PENDENTE"
    assert venda_com_itens["cliente_id"] == cliente["id"]
    assert venda_com_itens["itens"][0]["produto_id"] == produto_X["id"]
    assert venda_com_itens["itens"][1]["produto_id"] == produto_Y["id"]

    estoque1_produto_X = buscar_produto_por_id(client, token, produto_X["id"])
    estoque1_produto_Y = buscar_produto_por_id(client, token, produto_Y["id"])
    assert estoque1_produto_X["estoque"] == 9
    assert estoque1_produto_Y["estoque"] == 8

    fazer_pagamento_venda(client, token, venda_com_itens["id"], 300.0)

    venda1_paga = buscar_venda_por_id(client, token, venda_com_itens["id"])
    assert venda1_paga["status"] == "PAGO"
    assert venda1_paga["total_pago"] == 300.0

    fechar_venda_mes(client, token)

    listar1_vendas_fechadas_mes = listar_vendas_fechadas(client, token, mes=6, ano=2026)
    assert any(v["id"] == venda1_paga["id"] for v in listar1_vendas_fechadas_mes)

    cliente_inativado = inativar_cliente(client, token, cliente["id"])
    assert cliente_inativado["ativo"] == 0

    venda_invalida = criar_venda_simples_erro(client, token, cliente_id=cliente_inativado["id"])
    assert venda_invalida.status_code == 404

    cliente_reativado = reativar_cliente(client, token, cliente_inativado["id"])
    assert cliente_reativado["ativo"] == 1

    venda_valida = criar_venda_simples_por_cliente_id(client, token, cliente_id=cliente_reativado["id"])
    assert venda_valida["cliente_id"] == cliente_reativado["id"]

    produtoX_inativado = inativar_produto(client, token, produto_X["id"])
    assert produtoX_inativado["ativo"] == 0

    item_invalido = criar_item_e_adicionar_erro(client, token,
                                                venda_valida["id"],
                                                produto_X["id"])
    assert item_invalido.status_code == 404

    produtoX_reativado = reativar_produto(client, token, produto_X["id"])
    assert produtoX_reativado["ativo"] == 1

    item_valido = criar_item_e_adicionar_quantidade(client, token,
                                                    venda_valida["id"],
                                                    produtoX_reativado["id"],
                                                    quantidade=1)
    assert item_valido["itens"][0]["produto_id"] == produtoX_reativado["id"]
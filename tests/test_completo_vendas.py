from tests.helpers.produtos import (
                                    criar_produto,
                                    buscar_produto_por_id,
                                    inativar_produto
                                    )

from tests.helpers.clientes import (
                                    criar_cliente,
                                    inativar_cliente
                                    )

from tests.helpers.vendas import (
                                    criar_venda_simples,
                                    criar_item_e_adicionar,
                                    buscar_venda_por_id,
                                    listar_vendas,
                                    fazer_pagamento_venda,
                                    atualizar_item,
                                    deletar_venda,
                                    fechar_venda_mes,
                                    listar_vendas_fechadas,
                                    criar_venda_simples_erro,
                                    criar_item_e_adicionar_erro
                                    )

def test_completo_vendas(client, token):

    venda_criada = criar_venda_simples(client, token)

    venda_id = venda_criada["id"]

    venda = buscar_venda_por_id(client, token, venda_id)
    assert venda["id"] == venda_id

    produto = criar_produto(client, token)
    assert produto["estoque"] == 5

    item_adicionado = criar_item_e_adicionar(client, token, venda["id"],produto["id"])

    venda_com_item = buscar_venda_por_id(client, token, item_adicionado["id"])
    assert len(venda_com_item["itens"]) == 1
    assert venda_com_item["status"] == "PENDENTE"
    assert venda_com_item["total"] == 10.5

    estoque_atualizado = buscar_produto_por_id(client, token, produto["id"])
    assert estoque_atualizado["estoque"] == 4

    fazer_pagamento_venda(client, token, venda_com_item["id"], 10.5)

    venda_paga = buscar_venda_por_id(client, token, venda_com_item["id"])
    assert venda_paga["status"] == "PAGO"
    assert venda_paga["total_pago"] == 10.5

    data = deletar_venda(client, token, venda_paga["id"])
    assert data.status_code == 422

    fechar_venda_mes(client, token)

    vendas_fechadas = listar_vendas_fechadas(client, token, mes=6, ano=2026)
    assert any(v["id"] ==  venda_paga["id"] for v in vendas_fechadas)

    nova_venda = criar_venda_simples(client, token)

    item_novo = criar_item_e_adicionar(client, token, nova_venda["id"], produto["id"])
    
    venda_nova_com_item = buscar_venda_por_id(client, token, item_novo["id"])
    assert len(venda_nova_com_item["itens"]) == 1
    assert venda_nova_com_item["status"] == "PENDENTE"
    assert venda_nova_com_item["total"] == 10.5

    estoque_atualizado2 = buscar_produto_por_id(client, token, estoque_atualizado["id"])
    assert estoque_atualizado2["estoque"] == 3

    fazer_pagamento_venda(client, token, venda_nova_com_item["id"], 5.0)
    
    venda_nova_paga_parcial = buscar_venda_por_id(client, token, venda_nova_com_item["id"])
    assert venda_nova_paga_parcial["status"] == "PARCIAL"
    assert venda_nova_paga_parcial["total_pago"] == 5.0

    data = deletar_venda(client, token, venda_nova_paga_parcial["id"])
    assert data.status_code == 422

    atualizar_item(client, token, venda_nova_paga_parcial["id"], produto["id"],quantidade=2)

    venda_nova_item_atualizado = buscar_venda_por_id(client, token, venda_nova_paga_parcial["id"])
    assert venda_nova_item_atualizado["itens"][0]["quantidade"] == 2
    assert venda_nova_item_atualizado["total"] == 21.0
    assert venda_nova_item_atualizado["status"] == "PARCIAL" 
    assert venda_nova_item_atualizado["total_pago"] == 5.0
    
    estoque_atualizado3 = buscar_produto_por_id(client, token, estoque_atualizado2["id"])
    assert estoque_atualizado3["estoque"] == 2

    atualizar_item(client, token, venda_nova_item_atualizado["id"], produto["id"],quantidade=1)

    venda_nova_item_reatualizada = buscar_venda_por_id(client, token, venda_nova_paga_parcial["id"])
    assert venda_nova_item_reatualizada["itens"][0]["quantidade"] == 1
    assert venda_nova_item_reatualizada["total"] == 10.5
    assert venda_nova_item_reatualizada["status"] == "PARCIAL" 
    assert venda_nova_item_reatualizada["total_pago"] == 5.0
    
    estoque_atualizado4 = buscar_produto_por_id(client, token, estoque_atualizado3["id"])
    assert estoque_atualizado4["estoque"] == 3


    fazer_pagamento_venda(client, token, venda_nova_item_reatualizada["id"], 5.5)

    fechar_venda_mes(client, token)

    vendas_fechadas2 = listar_vendas_fechadas(client, token, mes=6, ano=2026) 
    assert any(v["id"] == venda_nova_item_reatualizada["id"] for v in vendas_fechadas2)

    nova_venda3 = criar_venda_simples(client, token)

    item_novo3 = criar_item_e_adicionar(client, token, nova_venda3["id"], produto["id"])

    venda_novo3 = buscar_venda_por_id(client, token, item_novo3["id"])
    assert venda_novo3["itens"][0]["quantidade"] == 1
    assert venda_novo3["status"] == "PENDENTE"
    
    estoque_atualizado3 = buscar_produto_por_id(client, token, produto["id"])
    assert estoque_atualizado3["estoque"] == 2

    data = deletar_venda(client, token, venda_novo3["id"])
    assert data.status_code == 200

    vendas = listar_vendas(client, token)
    assert not any(v["id"] == venda_novo3["id"] for v in vendas)

    cliente = criar_cliente(client, token)

    cliente_inativado = inativar_cliente(client, token, cliente["id"])
    assert cliente_inativado["ativo"] is False

    venda_clinte_inativo = criar_venda_simples_erro(client, token, cliente_id=cliente_inativado["id"])
    assert venda_clinte_inativo.status_code == 404

    produto_inativado = inativar_produto(client, token, produto["id"])
    assert produto_inativado["ativo"] is False

    venda_criada_cliente_ativo = criar_venda_simples(client, token)

    item_produto_inativo = criar_item_e_adicionar_erro(client, token,
                                                        venda_criada_cliente_ativo["id"],
                                                        produto_inativado["id"])

    assert item_produto_inativo.status_code == 404
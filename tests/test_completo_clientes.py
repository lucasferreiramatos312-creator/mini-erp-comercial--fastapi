from tests.helpers.clientes import (
                                    criar_cliente_com_nome_email_telefone,
                                    buscar_cliente_por_id,
                                    buscar_cliente_por_nome,
                                    listar_clientes_ativos,
                                    atualizar_cliente,
                                    inativar_cliente,
                                    listar_clientes_inativos,
                                    reativar_cliente)


def test_de_fluxo_completo_clientes(client, token):

    criar_cliente = criar_cliente_com_nome_email_telefone(client, token,
                                                         nome="João Dias",
                                                         email="joao.dias@email.com",
                                                         telefone="11987654321"
                                                         )
    
    criar_cliente_invalido = criar_cliente_com_nome_email_telefone(client, token,
                                                                   nome=None,
                                                                   email=None,
                                                                   telefone="str"
                                                                   )
    
    assert criar_cliente_invalido.status_code == 422
    
    assert criar_cliente.status_code == 200

    novo_cliente = criar_cliente.json()["dados"]

    buscar_cliente_nome = buscar_cliente_por_nome(client, token, "João Dias")

    assert any(c["nome"] == "João Dias" for c in buscar_cliente_nome)

    buscar_cliente_id = buscar_cliente_por_id(client, token, novo_cliente["id"])

    assert buscar_cliente_id["id"] == novo_cliente["id"]

    clientes_ativos = listar_clientes_ativos(client, token)

    assert any(c["id"] == buscar_cliente_id["id"] for c in clientes_ativos)

    cliente_foi_atualizado = atualizar_cliente(client, token,
                                          nome="João Dias Silva",
                                          email="joaodiassilva@email.com",
                                          telefone="11975845450"
                                         )
                                         
    cliente_atualizado_invalido = atualizar_cliente(client, token,
                                          nome="  ",
                                          email="emailinvalido",
                                          telefone=None
                                         )
    
    assert cliente_atualizado_invalido.status_code == 422

    assert cliente_foi_atualizado.status_code == 200

    cliente_atualizado = cliente_foi_atualizado.json()["dados"]

    assert cliente_atualizado["nome"] == "João Dias Silva"
    assert cliente_atualizado["email"] == "joaodiassilva@email.com"
    assert cliente_atualizado["telefone"] == "11975845450"

    cliente_inativado = inativar_cliente(client, token, cliente_atualizado["id"])

    assert cliente_inativado["ativo"] is False

    clientes_inativos = listar_clientes_inativos(client, token)

    assert any(c["id"] == cliente_atualizado["id"] for c in clientes_inativos)

    cliente_reativado = reativar_cliente(client, token, cliente_inativado["id"])

    assert cliente_reativado["ativo"] is True

    clientes_ativos = listar_clientes_ativos(client, token)

    assert any(c["id"] == cliente_reativado["id"] for c in clientes_ativos)
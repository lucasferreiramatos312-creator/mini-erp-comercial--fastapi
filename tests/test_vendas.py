import pytest

from helpers.auth import headers, headers_sem_token

from helpers.clientes import criar_cliente

from helpers.produtos import criar_produto,buscar_produto_por_id

from helpers.vendas import (
                            criar_venda_completa,
                            criar_venda_simples,
                            criar_item_e_adicionar,
                            buscar_venda_por_id,
                            listar_vendas,
                            atualizar_item_venda,
                            fazer_pagamento_venda,
                            deletar_venda,
                            fechar_venda_mes,
                            listar_vendas_fechadas)


def test_criar_venda_completa_valido(client, token):

    cliente = criar_cliente(client, token)
    produto = criar_produto(client, token)

    
    response = client.post(
        "/vendas",
        headers=headers(token),
        json={
            "cliente_id": cliente["id"],
            "itens": [
                {
                    "produto_id": produto["id"],
                    "quantidade": 1,
                }]
            }
    )

    venda =  response.json()["dados"]
    venda_id = venda["id"]

    data = buscar_venda_por_id(client, token, venda_id)

    assert response.status_code == 200
    assert data["id"] == venda_id
    assert data["cliente_id"] == cliente["id"]
    assert data["status"] == "PENDENTE"
    assert len(data["itens"]) == 1
    assert data["itens"][0]["produto_id"] == produto["id"]

def test_criar_venda_simples_valido(client, token):

    cliente = criar_cliente(client,token)

    response = client.post(
        "/vendas/simples",
        headers=headers(token),
        json={
            "cliente_id": cliente["id"],
            "itens": []
        }
    )

    venda_id = response.json()["dados"]["id"]

    data = buscar_venda_por_id(client, token, venda_id)

    assert response.status_code == 200
    assert data["id"] == venda_id
    assert data["cliente_id"] == cliente["id"]
    assert data["status"] == "PENDENTE"
    assert len(data["itens"]) == 0

def test_criar_item_venda(client, token):

    produto = criar_produto(client, token)
    
    venda = criar_venda_simples(client, token)

    venda_id = venda["id"]

    response = client.post(
        f"/vendas/{venda_id}/itens",
        headers=headers(token),
        json={
            "produto_id": produto["id"],
            "quantidade": 1,
        }
    )

    data = buscar_venda_por_id(client, token, venda_id)

    assert response.status_code == 200
    assert data["id"] == venda_id
    assert data["cliente_nome"] == "Cliente Teste"
    assert data["status"] == "PENDENTE"
    assert len(data["itens"]) == 1
    assert data["itens"][0]["produto_id"] == produto["id"]

def test_fazer_pagamento_total_valido(client, token):

    venda = criar_venda_completa(client, token)
    venda_id = venda["id"]

    response = client.post(
        f"/vendas/{venda_id}/pagamentos",
        headers=headers(token),
        json={
            "valor_pago": 10.5
        }
    )
    assert response.status_code == 200

    data = buscar_venda_por_id(client, token, venda_id)

    assert data["id"] == venda_id
    assert data["cliente_nome"] == "Cliente Teste"
    assert data["status"] == "PAGO"
    assert data["total_pago"] == 10.5
    assert len(data["itens"]) == 1
    assert data["itens"][0]["produto_nome"] == "Produto Teste"
 
def test_fazer_pagamento_parcial_valido(client, token):

    venda = criar_venda_completa(client, token)

    venda_id = venda["id"]

    response = client.post(
        f"/vendas/{venda_id}/pagamentos",
        headers=headers(token),
        json={
            "valor_pago": 5.25
        }
    )

    assert response.status_code  == 200

    data = buscar_venda_por_id(client, token, venda_id)

    assert data["id"] == venda_id
    assert data["cliente_nome"] == "Cliente Teste"
    assert data["total"] > 0
    assert data["status"] == "PARCIAL"
    assert data["total_pago"] == 5.25
    assert len(data["itens"]) == 1
    assert data["itens"][0]["produto_nome"] == "Produto Teste"
    assert data["itens"][0]["valor_unitario"] == 10.5 

def test_criar_venda_completa_token_invalido(client, token):

    cliente = criar_cliente(client, token)
    produto = criar_produto(client, token)

    response = client.post(
        "/vendas",
        headers=headers("token_invalido"),
        json={
            "cliente_id": cliente["id"],
            "itens": [
                {
                    "produto_id": produto["id"],
                    "quantidade": 1,
                }]
            }
    )

    assert response.status_code == 401

def test_criar_venda_simples_token_invalido(client, token):

    cliente = criar_cliente(client,token)

    response = client.post(
        "/vendas/simples",
        headers=headers("token_invalido"),
        json={
            "cliente_id": cliente["id"],
            "itens": []
        }
    )

    assert response.status_code == 401

def test_criar_item_venda_token_invalido(client, token):

    produto = criar_produto(client, token)
    
    venda = criar_venda_simples(client, token)

    venda_id = venda["id"]

    response = client.post(
        f"/vendas/{venda_id}/itens",
        headers=headers("token_invalido"),
        json={
            "produto_id": produto["id"],
            "quantidade": 1,
        }
    )

    assert response.status_code == 401

def test_fazer_pagamento_token_invalido(client, token):

    venda = criar_venda_completa(client, token)
    venda_id = venda["id"]

    response = client.post(
        f"/vendas/{venda_id}/pagamentos",
        headers=headers("token_invalido"),
        json={
            "valor_pago": 10.5
        }
    )
    assert response.status_code == 401

def test_criar_venda_completa_sem_token(client, token):

    cliente = criar_cliente(client, token)
    produto = criar_produto(client, token)

    response = client.post(
        "/vendas",
        headers=headers_sem_token(),
        json={
            "cliente_id": cliente["id"],
            "itens": [
                {
                    "produto_id": produto["id"],
                    "quantidade": 1,
                }]
            }
    )

    assert response.status_code == 401

def test_criar_venda_simples_sem_token(client, token):

    cliente = criar_cliente(client,token)

    response = client.post(
        "/vendas/simples",
        headers=headers_sem_token(),
        json={
            "cliente_id": cliente["id"],
            "itens": []
        }
    )

    assert response.status_code == 401

def test_criar_item_venda_sem_token(client, token):

    produto = criar_produto(client, token)
    
    venda = criar_venda_simples(client, token)

    venda_id = venda["id"]

    response = client.post(
        f"/vendas/{venda_id}/itens",
        headers=headers_sem_token(),
        json={
            "produto_id": produto["id"],
            "quantidade": 1,
        }
    )

    assert response.status_code == 401

def test_fazer_pagamento_sem_token(client, token):

    venda = criar_venda_completa(client, token)
    venda_id = venda["id"]

    response = client.post(
        f"/vendas/{venda_id}/pagamentos",
        headers=headers_sem_token(),
        json={
            "valor_pago": 10.5
        }
    )

    assert response.status_code == 401

def test_buscar_vendas_por_cliente(client, token):

    venda = criar_venda_completa(client, token)

    response = client.get(
        "/vendas?nome=Cliente Teste",
        headers=headers(token),
    )

    assert response.status_code == 200

    data = response.json()["dados"]

    assert len(data) > 0
    assert data[0]["id"] == venda["id"]
    assert any(v["id"] == venda["id"] for v in data)

def test_listar_vendas(client, token):

    venda = criar_venda_completa(client, token)

    response = client.get(
        "/vendas",
        headers=headers(token),
    )

    data = response.json()["dados"]

    assert len(data) > 0
    assert any(v["id"] == venda["id"] for v in data)

def test_buscar_venda_por_id(client, token):

    venda = criar_venda_completa(client, token)
    venda_id = venda["id"]

    response = client.get(
        f"/vendas/{venda_id}",
        headers=headers(token),
    )

    assert response.status_code == 200

    data = response.json()["dados"]

    assert data["id"] == venda["id"]
    assert data["status"] == "PENDENTE"
    assert len(data["itens"]) == 1
    assert data["itens"][0]["produto_id"] == venda["itens"][0]["produto_id"]

def test_buscar_vendas_por_cliente_sem_token(client, token):

    venda = criar_venda_completa(client, token)

    response = client.get(
        "/vendas?nome=Cliente Teste",
        headers=headers_sem_token()
    )

    assert response.status_code == 401

def test_listar_vendas_sem_token(client, token):

    venda = criar_venda_completa(client, token)

    response = client.get(
        "/vendas",
        headers=headers_sem_token()
    )

    assert response.status_code == 401

def test_atualizar_venda_adcionar_remover_item_e_verificar_estoque(client, token):

    venda_criada = criar_venda_simples(client, token)

    produto_criado = criar_produto(client, token)

    assert produto_criado["estoque"] == 5

    produto_id = produto_criado["id"]

    venda_id = venda_criada["id"]

    criar_item_e_adicionar(client, token, venda_id, produto_id)

    venda = buscar_venda_por_id(client, token, venda_id)

    assert len(venda["itens"]) == 1

    response = client.put(
        f"/vendas/{venda['id']}/itens/{produto_id}",
        headers=headers(token),
        json={
            "quantidade": 2
        }
    )

    assert response.status_code == 200

    data = response.json()["dados"]

    estoque_atualizada = buscar_produto_por_id(client, token, data["itens"][0]["produto_id"])
    assert estoque_atualizada["estoque"] == 3


    assert data["itens"][0]["quantidade"] == 2
    assert data["itens"][0]["produto_id"] == produto_id

    resposta = client.put(
        f"/vendas/{venda['id']}/itens/{produto_id}",
        headers=headers(token),
        json={
            "quantidade": 1
        }
    )

    assert resposta.status_code == 200

    venda_atualizada = resposta.json()["dados"]

    data = buscar_venda_por_id(client, token, venda_atualizada["id"])
    assert data["itens"][0]["quantidade"] == 1

    estoque_atualizado = buscar_produto_por_id(client, token, produto_id)
    assert estoque_atualizado["estoque"] == 4

@pytest.mark.parametrize("quantidade", [0, -1, None, "String"])
def test_atualizar_venda_item_quantidade_invalida(client, token, quantidade):

    response = atualizar_item_venda(client, token, quantidade=quantidade)

    assert response.status_code == 422

def test_atualizar_venda_item_token_invalido(client, token):

    venda_criada = criar_venda_simples(client, token)

    produto_criado = criar_produto(client, token)

    assert produto_criado["estoque"] == 5

    produto_id = produto_criado["id"]

    venda_id = venda_criada["id"]

    criar_item_e_adicionar(client, token, venda_id, produto_id)

    venda = buscar_venda_por_id(client, token, venda_id)

    response = client.put(
        f"/vendas/{venda['id']}/itens/{produto_id}",
        headers=headers("token_invalido"),
        json={
            "quantidade": 2
        }
    )

    assert response.status_code == 401

def test_atualizar_venda_item_quantidade_sem_token(client, token):

    venda = criar_venda_completa(client, token)

    response = client.put(
        f"/vendas/{venda['id']}/itens/{venda['itens'][0]['produto_id']}",
        headers=headers_sem_token(),
        json={
            "quantidade": 2
        }
    )

    assert response.status_code == 401

def test_deletar_venda_nao_paga_e_retornar_itens_ao_estoque(client, token):

    venda_criada = criar_venda_simples(client, token)

    produto_criado = criar_produto(client, token)

    assert produto_criado["estoque"] == 5

    produto_id = produto_criado["id"]

    venda_id = venda_criada["id"]

    criar_item_e_adicionar(client, token, venda_id, produto_id)

    produto = buscar_produto_por_id(client, token, produto_id)

    assert produto["estoque"] == 4

    venda_existe = buscar_venda_por_id(client, token, venda_id)

    assert venda_existe["id"] == venda_id
    assert venda_existe["status"] == "PENDENTE"

    response = client.delete(
        f"/vendas/{venda_id}",
        headers=headers(token)
    )

    assert response.status_code == 200

    venda_apagada = listar_vendas(client, token)

    assert not any(v["id"] == venda_id for v in venda_apagada)

    data = buscar_produto_por_id(client, token, produto_id)

    assert data["estoque"] == 5

def test_deletar_venda_parcial_e_verificar_estoque(client, token):

    venda_criada = criar_venda_completa(client, token)

    assert venda_criada["status"] == "PENDENTE"

    venda_id = venda_criada["id"]

    fazer_pagamento_venda(client, token, venda_id, valor=5.25)

    venda_parcial = buscar_venda_por_id(client, token, venda_id)

    assert venda_parcial["status"] == "PARCIAL"

    response = deletar_venda(client, token, venda_parcial["id"])

    assert response.status_code == 422

def test_deletar_venda_paga(client, token):
    
    venda = criar_venda_completa(client, token)

    assert venda["status"] == "PENDENTE"

    fazer_pagamento_venda(client, token, venda["id"], valor=10.5)

    venda_parcial = buscar_venda_por_id(client, token, venda["id"])

    assert venda_parcial["status"] == "PAGO"

    response = deletar_venda(client, token, venda_parcial["id"])

    assert response.status_code == 422

def test_deletar_venda_token_invalido(client,token):

    venda = criar_venda_completa(client, token)

    response = deletar_venda(client, "token_invalido", venda["id"])

    assert response.status_code == 401

def test_deletar_venda_sem_token(client, token):

    venda_criada = criar_venda_completa(client, token)

    venda_id = venda_criada["id"]

    response = client.delete(
        f"/vendas/{venda_id}",
        headers=headers_sem_token()
    )
    
    assert response.status_code == 401

def test_fechar_vendas_pagas_e_lista(client, token):

    venda1 = criar_venda_completa(client, token)
    venda2 = criar_venda_completa(client, token)
    venda3 = criar_venda_completa(client, token)

    venda_id1 = venda1["id"]
    venda_id2 = venda2["id"]
    venda_id3 = venda3["id"]

    fazer_pagamento_venda(client, token, venda_id1, valor=10.5)
    fazer_pagamento_venda(client, token, venda_id2, valor=5.25)

    venda1_paga = buscar_venda_por_id(client, token, venda_id1)
    assert venda1_paga["status"] == "PAGO"
    
    venda2_parcial = buscar_venda_por_id(client, token, venda_id2)
    assert venda2_parcial["status"] == "PARCIAL"
    
    venda3_pendente = buscar_venda_por_id(client, token, venda_id3)
    assert venda3_pendente["status"] == "PENDENTE"

    response = client.post(
        "/vendas/fechar-mes",
        headers=headers(token)
    )

    assert response.status_code == 200

    lista_vendas = listar_vendas(client, token)

    assert not any(v["id"] == venda1_paga["id"] for v in lista_vendas)

    data = listar_vendas_fechadas(client, token, mes=6, ano=2026)

    assert any(v["id"] == venda1_paga["id"] for v in data)
    assert data[0]["status"] == "FECHADA"

def test_fechar_vendas_pagas_token_invalido(client, token):

    venda_criada = criar_venda_completa(client, token)

    venda_id = venda_criada["id"]

    fazer_pagamento_venda(client, token, venda_id, valor=10.5)

    venda_paga = buscar_venda_por_id(client, token, venda_id)

    assert venda_paga["status"] == "PAGO"

    response = fechar_venda_mes(client, "token_invalido")

    assert response.status_code == 401
def test_fechar_vendas_pagas_sem_token(client, token):

    venda_criada = criar_venda_completa(client, token)

    venda_id = venda_criada["id"]

    fazer_pagamento_venda(client, token, venda_id, valor=10.5)

    venda_paga = buscar_venda_por_id(client, token, venda_id)

    assert venda_paga["status"] == "PAGO"

    response = client.post(
        "/vendas/fechar-mes",
        headers=headers_sem_token()
    )

    assert response.status_code == 401

def test_listar_vendas_fechadas_token_invalido(client, token):
    
    venda_criada = criar_venda_completa(client, token)

    venda_id = venda_criada["id"]

    fazer_pagamento_venda(client, token, venda_id, valor=10.5)

    venda_paga = buscar_venda_por_id(client, token, venda_id)
    assert venda_paga["status"] == "PAGO"

    response = client.get(
        "/vendas/fechar-mes?mes=5&ano=2026",
        headers=headers("token_invalido")
    )

    assert response.status_code == 401

def test_listar_vendas_fechadas_sem_token(client, token):
    
    venda_criada = criar_venda_completa(client, token)

    venda_id = venda_criada["id"]

    fazer_pagamento_venda(client, token, venda_id, valor=10.5)

    venda_paga = buscar_venda_por_id(client, token, venda_id)
    assert venda_paga["status"] == "PAGO"

    response = client.get(
        "/vendas/fechar-mes?mes=5&ano=2026",
        headers=headers_sem_token()
    )

    assert response.status_code == 401
from helpers.auth import headers

from helpers.clientes import criar_cliente

from helpers.produtos import criar_produto

def criar_venda_completa(client, token):

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
                }
            ]
        }
    )

    return response.json()["dados"]

def criar_venda_simples(client, token):

    cliente = criar_cliente(client,token)

    response = client.post(
        "/vendas/simples",
        headers=headers(token),
        json={
            "cliente_id": cliente["id"],
            "itens": []
        }
    )

    return response.json()["dados"]

def criar_venda_simples_por_cliente_id(client, token, cliente_id):

    response = client.post(
        "/vendas/simples",
        headers=headers(token),
        json={
            "cliente_id": cliente_id,
            "itens": []
        }
    )

    return response.json()["dados"]


def criar_item_e_adicionar(client, token, venda_id, produto_id):
    
    response = client.post(
        f"/vendas/{venda_id}/itens",
        headers=headers(token),
        json={
            "produto_id": produto_id,
            "quantidade": 1,
        }
    )

    return response.json()["dados"]
def criar_item_e_adicionar_quantidade(client, token, venda_id, produto_id, quantidade):
    
    response = client.post(
        f"/vendas/{venda_id}/itens",
        headers=headers(token),
        json={
            "produto_id": produto_id,
            "quantidade": quantidade
        }
    )

    return response.json()["dados"]



def criar_venda_e_item(client, token):

    venda = criar_venda_simples(client, token)

    produto = criar_produto(client, token)

    item = criar_item_e_adicionar(client, token, venda["id"], produto["id"])

    return venda, item

def buscar_venda_por_id(client, token, venda_id):

    response = client.get(
        f"/vendas/{venda_id}",
        headers=headers(token),
    )

    return response.json()["dados"]

def listar_vendas(client, token):

    response = client.get(
        "/vendas",
        headers=headers(token),
    )

    return response.json()["dados"]

def fazer_pagamento_venda(client, token, venda_id, valor):

    response = client.post(
        f"/vendas/{venda_id}/pagamentos",
        headers=headers(token),
        json={
            "valor_pago": valor
        }
    )
    
    return response.json()["dados"]

def atualizar_item_venda(client, token, quantidade):

    venda_criada = criar_venda_simples(client, token)

    produto_criado = criar_produto(client, token)

    produto_id = produto_criado["id"]

    venda_id = venda_criada["id"]

    criar_item_e_adicionar(client, token, venda_id, produto_id)

    venda = buscar_venda_por_id(client, token, venda_id)

    response = client.put(
        f"/vendas/{venda['id']}/itens/{produto_id}",
        headers=headers(token),
        json={
            "quantidade": quantidade
        }
    )

    return response

def atualizar_item(client,token, venda_id, produto_id, quantidade):

    response = client.put(
        f"/vendas/{venda_id}/itens/{produto_id}",
        headers=headers(token),
        json={
            "quantidade": quantidade
        }
    )

    return response

def deletar_venda(client, token, venda_id):

    response = client.delete(
        f"/vendas/{venda_id}",
        headers=headers(token)
    )

    return response

def fechar_venda_mes(client, token):
    
    response = client.post(
        "/vendas/fechar-mes",
        headers=headers(token)
    )

    return response

def listar_vendas_fechadas(client, token, mes=None, ano=None):

    response = client.get(
        f"/vendas/historico?mes={mes}&ano={ano}",
        headers=headers(token)
    )

    return response.json()["dados"]

def criar_venda_simples_erro(client, token, cliente_id):

    response = client.post(
        "/vendas/simples",
        headers=headers(token),
        json={
            "cliente_id": cliente_id,
            "itens": []
        }
    )

    return response

def criar_item_e_adicionar_erro(client, token, venda_id, produto_id):
    
    response = client.post(
        f"/vendas/{venda_id}/itens",
        headers=headers(token),
        json={
            "produto_id": produto_id,
            "quantidade": 1,
        }
    )

    return response
from helpers.auth import headers

def criar_produto(client, token):

    response = client.post(
        "/produtos",
        headers=headers(token),
        json={
            "nome": "Produto Teste",
            "valor": 10.5,
            "estoque": 5
        }
    )

    return response.json()["dados"]

def criar_produto_com_nome_valor_estoque(client, token, nome, valor, estoque):

    response = client.post(
        "/produtos",
        headers=headers(token),
        json={
            "nome": nome,
            "valor": valor,
            "estoque": estoque
        }
    )

    return response

def buscar_produto_por_id(client, token, produto_id):
    
    response = client.get(
        f"/produtos/{produto_id}",
        headers=headers(token)
    )

    return response.json()["dados"]

def buscar_produto_por_nome(client, token, nome):

    response = client.get(
        f"/produtos?nome={nome}",
        headers=headers(token)
    )

    return response.json()["dados"]

def listar_produtos_ativos(client, token):

    response = client.get(
        "/produtos",
        headers=headers(token)
    )

    return response.json()["dados"]

def atualizar_produto(client, token, nome, valor, estoque):

    produto = criar_produto(client, token)

    response = client.put(
        f"/produtos/{produto['id']}",
        headers=headers(token),
        json={
            "nome": nome,
            "valor": valor,
            "estoque": estoque
        }
    )

    return response

def inativar_produto(client, token, produto_id):

    response = client.put(
    f"/produtos/{produto_id}/inativar",
    headers=headers(token)
    )

    return response.json()["dados"]

def reativar_produto(client, token, produto_id):

    response = client.put(
        f"/produtos/{produto_id}/reativar",
        headers=headers(token)
    )

    return response.json()["dados"]

def listar_produtos_inativos(client, token):

    response = client.get(
        "/produtos/inativos",
        headers=headers(token)
    )

    return response.json()["dados"]
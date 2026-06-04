from helpers.auth import headers

def criar_cliente(client, token):

    response = client.post(
        "/clientes",
        headers=headers(token),
        json={
            "nome": "Cliente Teste",
            "email": "cliente@email.com",
            "telefone": "11999999999"
        }
    )

    return response.json()["dados"]

def criar_cliente_com_nome_email_telefone(client, token, nome, email, telefone):

    response = client.post(
        "/clientes",
        headers=headers(token),
        json={
            "nome": nome,
            "email": email,
            "telefone": telefone
        }
    )

    return response

def buscar_cliente_por_id(client, token, cliente_id):

    response = client.get(
        f"/clientes/{cliente_id}",
        headers=headers(token)
    )

    return response.json()["dados"]

def buscar_cliente_por_nome(client, token, nome):

    response = client.get(
        f"/clientes?nome={nome}",
        headers=headers(token)
    )

    return response.json()["dados"]

def listar_clientes_ativos(client, token):

    response = client.get(
        "/clientes",
        headers=headers(token)
    )

    return response.json()["dados"]

def atualizar_cliente(client, token, nome, email, telefone):

    cliente = criar_cliente(client, token)

    response = client.put(
        f"/clientes/{cliente['id']}",
        headers=headers(token),
        json={
            "nome": nome,
            "email": email,
            "telefone": telefone
        }
    )

    return response

def inativar_cliente(client, token, cliente_id):

    response = client.put(
    f"/clientes/{cliente_id}/inativar",
    headers=headers(token)
    )

    return response.json()["dados"]

def reativar_cliente(client, token, cliente_id):

    response = client.put(
        f"/clientes/{cliente_id}/reativar",
        headers=headers(token)
    )

    return response.json()["dados"]

def listar_clientes_inativos(client, token):

    response = client.get(
        "/clientes/inativos",
        headers=headers(token)
    )

    return response.json()["dados"]
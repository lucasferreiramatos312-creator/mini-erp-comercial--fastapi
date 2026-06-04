import pytest

from tests.helpers.auth import headers, headers_sem_token

from tests.helpers.clientes import (criar_cliente,
                                    criar_cliente_com_nome_email_telefone,
                                    buscar_cliente_por_id,
                                    atualizar_cliente,
                                    inativar_cliente)

def test_criar_cliente_valido(client, token):

    response = client.post(
        "/clientes",
        headers=headers(token),
        json={
            "nome": "Cliente Teste",
            "email": "cliente@email.com",
            "telefone": "11999999999"
        }
    )

    assert response.status_code == 200

def test_criar_cliente_token_invalido(client, token):

    response = client.post(
        "/clientes",
        headers=headers("token_invalido"),
        json={
            "nome": "Cliente Teste",
            "email": "cliente@email.com",
            "telefone": "11999999999"
        }
    )

    assert response.status_code == 401

def test_criar_cliente_sem_token(client, token):

    response = client.post(
        "/clientes",
        headers=headers_sem_token(),
        json={
            "nome": "Cliente Teste",
            "email": "cliente@email.com",
            "telefone": "11999999999"
        }
    )

    assert response.status_code == 401

@pytest.mark.parametrize("nome", ["", "  ", None])
def test_criar_cliente_nome_invalido(client, token, nome):

    response = criar_cliente_com_nome_email_telefone(client, token, nome=nome,
                                                     email="cliente@email.com",
                                                     telefone="11999999999")

    assert response.status_code == 422

@pytest.mark.parametrize("email", ["", "  ", "clienteemail.com", 123456, None])
def test_criar_cliente_com_email_invalido(client, token, email):

    response = criar_cliente_com_nome_email_telefone(client, token,
                                                     nome= "Cliente Teste",
                                                     email=email,
                                                     telefone="11999999999")

    assert response.status_code == 422

@pytest.mark.parametrize("telefone", ["", "  ", "1199999999999999999999", "119", "string", None])
def test_criar_cliente_telefone_invalido(client, token, telefone):

    response = criar_cliente_com_nome_email_telefone(client, token,
                                                     nome= "Cliente Teste",
                                                     email="cliente@email.com",
                                                     telefone=telefone)

    assert response.status_code == 422

def test_listar_clientes(client, token):

    cliente = criar_cliente(client, token)

    response = client.get(
        "/clientes",
        headers=headers(token)
    )

    assert response.status_code == 200

    data = response.json()["dados"]

    assert len(data) > 0

    assert any(c["id"] == cliente["id"] for c in data)

def test_buscar_cliente_por_nome(client, token):

    cliente = criar_cliente(client, token)

    response = client.get(
        "/clientes?nome=Cliente Teste",
        headers=headers(token)
    )

    assert response.status_code == 200

    data = response.json()["dados"]

    assert any(c["nome"] == "Cliente Teste" for c in data)

def test_buscar_cliente_por_id(client, token):

    cliente = criar_cliente(client, token)

    response = client.get(
        f"/clientes/{cliente['id']}",
        headers=headers(token)
    )

    assert response.status_code == 200

    data = response.json()["dados"]

    assert data["id"] == cliente["id"]

def test_atualizar_cliente_todos_campos_validos(client, token):

    cliente = criar_cliente(client, token)

    assert cliente["nome"] == "Cliente Teste"
    assert cliente["email"] == "cliente@email.com"
    assert cliente["telefone"] == "11999999999"

    response = client.put(
        f"/clientes/{cliente['id']}",
        headers=headers(token),
        json={
            "nome": "Cliente atualizado",
            "email": "cliente@emailatualizado.com",
            "telefone": "11888888888"
        }
    )

    assert response.status_code == 200

    data = buscar_cliente_por_id(client, token, cliente["id"])

    assert data["nome"] == "Cliente atualizado"
    assert data["email"] == "cliente@emailatualizado.com"
    assert data["telefone"] == "11888888888"

@pytest.mark.parametrize("nome", ["", "   ", None])
def test_atualizar_cliente_nome_invalido(client, token, nome):

    reponse = atualizar_cliente(client, token,
                                nome=nome,
                                email="cliente@email.com",
                                telefone="11999999999")

    assert reponse.status_code == 422

@pytest.mark.parametrize("email", ["", "   ", "clienteemail.com", "@#$!%&*", 123456, None])
def test_atualizar_cliente_email_invalido(client, token, email):

    response = atualizar_cliente(client, token,
                                 nome="Cliente Teste",
                                 email=email,
                                 telefone="11999999999")

    assert response.status_code == 422

@pytest.mark.parametrize("telefone", ["", "   ", "119999999999999", "119", "string", None])
def test_atualizar_cliente_telefone_string(client, token, telefone):

    response = atualizar_cliente(client, token,
                                 nome="Cliente Teste",
                                 email="cliente@email.com",
                                 telefone=telefone)

    assert response.status_code == 422

def test_inativar_cliente(client, token):

    cliente= criar_cliente(client, token)
    
    response = client.put(
        f"/clientes/{cliente['id']}/inativar",
        headers=headers(token)
    )

    assert response.status_code == 200

    data = buscar_cliente_por_id(client, token, cliente["id"])

    assert response.json()["dados"]["ativo"] == 0

    assert data["id"] == response.json()["dados"]["id"]

def test_listar_clientes_inativos(client, token):

    cliente_ativo = criar_cliente(client, token)
        
    cliente_inativado = inativar_cliente(client, token, cliente_ativo["id"])

    response = client.get(
        "/clientes/inativos",
        headers=headers(token)
    )

    assert response.status_code == 200

    data = response.json()["dados"]

    assert len(data) > 0

    assert any(c["id"] == cliente_inativado["id"] for c in data)

def test_reativar_cliente(client, token):

    cliente_ativo = criar_cliente(client, token)

    cliente_inativo = inativar_cliente(client, token, cliente_ativo["id"])

    assert cliente_inativo["ativo"] == 0

    response = client.put(
        f"/clientes/{cliente_inativo['id']}/reativar",
        headers=headers(token)
    )

    assert response.status_code == 200

    data = response.json()["dados"]

    assert data["ativo"] == 1
    assert data["id"] == cliente_inativo["id"]
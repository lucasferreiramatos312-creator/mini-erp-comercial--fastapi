import pytest

from helpers.auth import headers,headers_sem_token 

from tests.helpers.produtos import(
    criar_produto,
    criar_produto_com_nome_valor_estoque,
    buscar_produto_por_id,
    atualizar_produto,
    inativar_produto
)

def test_criar_produto_valido(client, token):
    
    response = client.post(
        "/produtos",
        headers=headers(token),
        json={
            "nome": "Produto Teste",
            "valor": 10.5,
            "estoque": 5
        }
    )

    assert response.status_code == 200

def test_criar_produto_token_invalido(client):

    response = client.post(
        "/produtos",
        headers=headers("token_invalido"),
        json={
            "nome": "Produto Teste",
            "valor": 10.5,
            "estoque": 5
        }
    )

    assert response.status_code == 401

def test_criar_produtos_sem_token(client):

    response = client.post(
        "/produtos",
        headers=headers_sem_token(),
        
        json={
            "nome": "Produto Teste",
            "valor": 10.5,
            "estoque": 5
        }
    )

    assert response.status_code == 401

@pytest.mark.parametrize("nome", ["", "   ", None])
def test_criar_produto_sem_nome(client, token, nome):

    response = criar_produto_com_nome_valor_estoque(client, token, nome=nome, valor=10.5, estoque=5)

    assert response.status_code == 422

@pytest.mark.parametrize("valor", ["", "   ", 0, -10.5, "String", None])
def test_criar_produto_com_valor_invalido(client, token, valor):

    response = criar_produto_com_nome_valor_estoque(client, token, nome="Produto Teste", valor=valor, estoque=5)

    assert response.status_code == 422

def test_criar_produto_com_estoque_zarado(client, token):

    response = criar_produto_com_nome_valor_estoque(client, token, nome="Produto Teste", valor=10.5, estoque=0)

    assert response.status_code == 200

@pytest.mark.parametrize("estoque", ["", "   ", -5, "String", None])
def test_criar_produto_com_estoque_negativo(client, token, estoque):

    response = criar_produto_com_nome_valor_estoque(client, token, nome="Produto Teste", valor=10.5, estoque=estoque)

    assert response.status_code == 422

def test_listar_produtos(client, token):

    produto = criar_produto(client, token)

    response = client.get(
        "/produtos",
        headers=headers(token)
    )

    assert response.status_code == 200

    data = response.json()["dados"]

    assert len(data) > 0

    assert any(p["id"] == produto["id"] for p in data)
    
def test_buscar_produto_por_nome(client,token):

    response = client.get(
        "/produtos?nome=Produto Teste",
        headers=headers(token)
    )

    assert response.status_code == 200


    data = response.json()["dados"]

    assert any(c["nome"] == "Produto Teste" for c in data)


def test_atualizar_produto_todos_campos(client, token):

    produto = criar_produto(client, token)
    
    response = client.put(
        f"/produtos/{produto['id']}",
        headers=headers(token),
        json={
            "nome": "Produto atualizado",
            "valor": 20.5,
            "estoque": 10
        }
    )

    assert response.status_code == 200

    data = buscar_produto_por_id(client, token, produto["id"])

    assert data["nome"] == "Produto atualizado"    
    assert data["valor"] == 20.5
    assert data["estoque"] == 10

@pytest.mark.parametrize("nome", ["", "   ", None])
def test_atualizar_produto_nome_invalido(client, token, nome):

    response = atualizar_produto(client, token, nome=nome, valor=20.5, estoque=5)

    assert response.status_code == 422

@pytest.mark.parametrize("valor", ["", "   ", 0, -10.5, "String", None])
def test_atualizar_produto_valor_invalido(client, token, valor):

    response = atualizar_produto(client, token, nome="Produto Teste", valor=valor, estoque=5)

    assert response.status_code == 422

def test_atualizar_produto_estoque_zerado(client, token):

    produto = criar_produto(client, token)

    response = client.put(
        f"/produtos/{produto['id']}",
        headers=headers(token),
        json={
            "nome": "Produto estoque1",
            "valor": 10.5,
            "estoque": 0
        }
    )

    assert response.status_code == 200

    assert response.json()["dados"]["estoque"] == 0

@pytest.mark.parametrize("estoque", ["", "   ", -5, "String", None])
def test_atualizar_produto_estoque_invalido(client, token, estoque):

    response = atualizar_produto(client, token,nome="Produto Teste", valor=20.5, estoque=estoque)
    
    assert response.status_code == 422
    
def test_inativar_produto(client, token):

    produto = criar_produto(client, token)

    response = client.put(
        f"/produtos/{produto['id']}/inativar",
        headers=headers(token)
    )

    assert response.status_code == 200
    
    assert response.json()["dados"]["ativo"] is False

def test_listar_produtos_inativos(client, token):

    produto_ativo = criar_produto(client, token)
        
    produto_inativado = inativar_produto(client, token, produto_ativo["id"])

    response = client.get(
        "/produtos/inativos",
        headers=headers(token)
    )

    assert response.status_code == 200

    data = response.json()["dados"]

    assert len(data) > 0

    assert any(p["id"] == produto_inativado["id"] for p in data)

def test_reativar_produto(client, token):

    produto_ativo = criar_produto(client, token)

    produto_inativo = inativar_produto(client, token, produto_ativo["id"])
    
    response = client.put(
        f"/produtos/{produto_inativo['id']}/reativar",
        headers=headers(token)
    )

    assert response.status_code == 200

    assert response.json()["dados"]["ativo"] is True

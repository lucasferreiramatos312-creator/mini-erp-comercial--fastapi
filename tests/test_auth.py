from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_login_invalido():

    response = client.post(
        "/auth/login",
        json={
            "email": "testeinvalido@email.com",
            "senha": "123456"
        }
    )

    assert response.status_code == 401

def test_login_valido():

    response = client.post(
        "/auth/login",
        json={
            "email": "teste@email.com",
            "senha": "123456"
        } 
    )

    assert response.status_code == 200

def test_token_invalido():

    response = client.get(
        "/produtos",
        headers={
            "Authorization": "Bearer token_falso"
        }
    )

    assert response.status_code == 401

def test_sem_token():

    response = client.get("/produtos")

    assert response.status_code == 401
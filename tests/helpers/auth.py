from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def obter_token():

    login = client.post(
        "/auth/login",
        json={
            "email": "teste@email.com",
            "senha": "123456"
        }
    )

    return login.json()["dados"] ["access_token"]

def headers(token):

    return {
        "Authorization": f"Bearer {token}"
    }

def headers_sem_token():

    return {
        "Authorization": f"Bearer "
    }

def headers_token_invalido(token_invalido):

    return {
        "Authorization": f"Bearer {token_invalido}"
    }

def criar_usuario():

    response = client.post(
        "/auth/registrar",
        json={
            "nome": "Teste De Sistema Completo",
            "email": "testecompleto@email.com",
            "senha": "123456"
        }
    )

    return response

def login_usuario():
    
    login = client.post(
        "/auth/login",
        json={
            "email": "testecompleto@email.com",
            "senha": "123456"
        }
    )

    return login.json()["dados"] ["access_token"]
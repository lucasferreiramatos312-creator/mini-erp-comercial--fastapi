import pytest
from fastapi.testclient import TestClient

from main import app
from helpers.auth import obter_token

client = TestClient(app)

@pytest.fixture
def token():
    return obter_token()

@pytest.fixture
def client():
    return TestClient(app)
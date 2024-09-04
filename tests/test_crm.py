from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_client_creating():
    response = client.post('/clients/')
    assert response.status_code == 200


def test_failed_creating():
    value = client.post('/clients/')
    assert value.status_code == 404
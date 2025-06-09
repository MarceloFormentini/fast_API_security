from fastapi.testclient import TestClient
import pytest
from app.main import app

@pytest.fixture(scope="session")
def client():
    return TestClient(app)

@pytest.fixture(scope="module")
def auth_cookies(client):
    # Cria usuário e faz login, retorna cookies e token
    client.post("/register", json={"username":"user1", "password":"pass"})
    login = client.post(
        "/login",
        data={"username":"user1", "password":"pass"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert login.status_code == 200
    cookies = login.cookies
    token = login.json()["access_token"]
    return {"cookies": cookies, "token": token}
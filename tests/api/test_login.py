from fastapi.testclient import TestClient

from app.settings import settings


def test_get_access_token(client: TestClient) -> None:
    login_data = {
        'username': settings.super_user_email,
        'password': settings.super_user_password,
    }
    r = client.post('/auth/access-token', data=login_data)
    assert r.status_code == 200
    tokens = r.json()
    assert "access_token" in tokens
    assert tokens["access_token"]

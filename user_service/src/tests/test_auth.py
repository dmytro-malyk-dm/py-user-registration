import pytest
from httpx import AsyncClient
from unittest.mock import patch


@pytest.fixture(autouse=True)
def mock_password_hashing():

    with patch("user_service.src.security.password.pwd_context.hash") as mock_hash:
        mock_hash.side_effect = lambda p: f"hashed_{p}"
        with patch("user_service.src.security.password.pwd_context.verify") as mock_verify:
            mock_verify.side_effect = lambda p, h: h == f"hashed_{p}"
            yield


VALID_USER = {
    "name": "John",
    "surname": "Doe",
    "email": "john@example.com",
    "date_of_birthday": "1990-01-15",
    "password": "Secure123!",
}


@pytest.mark.asyncio
async def test_register_success(client: AsyncClient):
    response = await client.post("/api/v1/user/register/", json=VALID_USER)

    assert response.status_code == 201
    assert response.json()["message"] == "User registered successfully"


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient):
    await client.post("/api/v1/user/register/", json=VALID_USER)
    response = await client.post("/api/v1/user/register/", json=VALID_USER)

    assert response.status_code == 400
    assert "already exist" in response.json()["detail"]


@pytest.mark.asyncio
async def test_register_invalid_email(client: AsyncClient):
    payload = {**VALID_USER, "email": "not-an-email"}
    response = await client.post("/api/v1/user/register/", json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient):
    await client.post("/api/v1/user/register/", json=VALID_USER)

    response = await client.post(
        "/api/v1/user/login/",
        json={"email": VALID_USER["email"], "password": VALID_USER["password"]},
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient):
    await client.post("/api/v1/user/register/", json=VALID_USER)

    response = await client.post(
        "/api/v1/user/login/",
        json={"email": VALID_USER["email"], "password": "WrongPassword123!"},
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Incorrect email or password"


@pytest.mark.asyncio
async def test_login_nonexistent_user(client: AsyncClient):
    response = await client.post(
        "/api/v1/user/login/",
        json={"email": "ghost@example.com", "password": "Password123!"},
    )

    assert response.status_code == 401

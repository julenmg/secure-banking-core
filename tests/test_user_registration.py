import pytest
from httpx import AsyncClient

REGISTER_URL = "/api/v1/users/register"


@pytest.mark.asyncio
async def test_register_user_success(client: AsyncClient):
    payload = {"email": "alice@example.com", "username": "alice", "password": "securepass1"}
    response = await client.post(REGISTER_URL, json=payload)

    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "alice@example.com"
    assert body["username"] == "alice"
    assert body["is_active"] is True
    assert "id" in body
    assert "created_at" in body
    assert "hashed_password" not in body


@pytest.mark.asyncio
async def test_register_normalizes_username_to_lowercase(client: AsyncClient):
    payload = {"email": "bob@example.com", "username": "BobUser", "password": "securepass1"}
    response = await client.post(REGISTER_URL, json=payload)

    assert response.status_code == 201
    assert response.json()["username"] == "bobuser"


@pytest.mark.asyncio
async def test_register_duplicate_email_returns_409(client: AsyncClient):
    payload = {"email": "carol@example.com", "username": "carol", "password": "securepass1"}
    await client.post(REGISTER_URL, json=payload)

    payload2 = {"email": "carol@example.com", "username": "carol2", "password": "securepass1"}
    response = await client.post(REGISTER_URL, json=payload2)

    assert response.status_code == 409
    assert "Email already registered" in response.json()["detail"]


@pytest.mark.asyncio
async def test_register_duplicate_username_returns_409(client: AsyncClient):
    payload = {"email": "dave@example.com", "username": "dave", "password": "securepass1"}
    await client.post(REGISTER_URL, json=payload)

    payload2 = {"email": "dave2@example.com", "username": "dave", "password": "securepass1"}
    response = await client.post(REGISTER_URL, json=payload2)

    assert response.status_code == 409
    assert "Username already taken" in response.json()["detail"]


@pytest.mark.asyncio
async def test_register_invalid_email_returns_422(client: AsyncClient):
    payload = {"email": "not-an-email", "username": "eve", "password": "securepass1"}
    response = await client.post(REGISTER_URL, json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_short_password_returns_422(client: AsyncClient):
    payload = {"email": "frank@example.com", "username": "frank", "password": "short"}
    response = await client.post(REGISTER_URL, json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_short_username_returns_422(client: AsyncClient):
    payload = {"email": "grace@example.com", "username": "gr", "password": "securepass1"}
    response = await client.post(REGISTER_URL, json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_register_username_with_special_chars_returns_422(client: AsyncClient):
    payload = {"email": "henry@example.com", "username": "henry!!", "password": "securepass1"}
    response = await client.post(REGISTER_URL, json=payload)

    assert response.status_code == 422


@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    response = await client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

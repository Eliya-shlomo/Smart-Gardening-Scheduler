import pytest
from httpx import AsyncClient, ASGITransport
from backend.main import app

async def register_and_login(client: AsyncClient, email="test@example.com", password="12345678"):
    register_data = {
        "email": email,
        "password": password,
        "name": "Test User",
        "phone": "0501234567"
    }
    await client.post("/users/register", json=register_data)

    login_data = {
        "email": email,
        "password": password
    }
    res = await client.post("/users/login", json=login_data)
    assert res.status_code == 200
    token = res.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_create_get_update_client(client):
    headers = await register_and_login(client)

    create_data = {
        "name": "לקוח בדיקה",
        "email": "client@example.com",
        "address": "רחוב הבדיקה 12",
        "phone": "0501234567"
    }

    res = await client.post("/clients/", json=create_data, headers=headers)
    assert res.status_code == 200
    data = res.json()
    assert data["name"] == create_data["name"]
    assert data["email"] == create_data["email"]
    assert "id" in data

    client_id = data["id"]

    res = await client.get(f"/clients/{client_id}", headers=headers)
    assert res.status_code == 200
    fetched = res.json()
    assert fetched["id"] == client_id
    assert fetched["email"] == create_data["email"]

    update_data = {
        "name": "לקוח מעודכן",
        "email": "client@example.com",
        "address": "רחוב אחר 45",
        "phone": "0527654321"
    }

    res = await client.put(f"/clients/{client_id}", json=update_data, headers=headers)
    assert res.status_code == 200
    updated = res.json()
    assert updated["name"] == update_data["name"]
    assert updated["address"] == update_data["address"]
    assert updated["phone"] == update_data["phone"]

@pytest.mark.asyncio
async def test_create_client_missing_fields(client):
    headers = await register_and_login(client)

    bad_data = {
        "email": "bad@example.com",
        "address": "רחוב כלשהו",
        "phone": "0500000000"
    }

    res = await client.post("/clients/", json=bad_data, headers=headers)
    assert res.status_code == 422

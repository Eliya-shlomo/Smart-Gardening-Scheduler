import pytest
from httpx import AsyncClient

CLIENTS_URL = "http://localhost:8002"
USERS_URL = "http://localhost:8001"

async def register_and_login(email="test@example.com", password="12345678"):
    async with AsyncClient(base_url=USERS_URL) as client:
        await client.post("/users/register", json={
            "email": email,
            "password": password,
            "name": "Test User",
            "phone": "0501234567"
        })
        login = await client.post("/users/login", json={
            "email": email,
            "password": password
        })
        assert login.status_code == 200
        token = login.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

@pytest.mark.asyncio
async def test_create_get_update_delete_client():
    headers = await register_and_login()
    async with AsyncClient(base_url=CLIENTS_URL) as client:
        # יצירה
        create_data = {
            "name": "לקוח בדיקה",
            "email": "client@example.com",
            "address": "רחוב הבדיקה 12",
            "phone": "0501234567"
        }
        res = await client.post("/clients/", json=create_data, headers=headers)
        assert res.status_code == 200
        client_id = res.json()["id"]

        res = await client.get(f"/clients/{client_id}", headers=headers)
        assert res.status_code == 200

        update_data = {
            "name": "לקוח מעודכן",
            "email": "client@example.com",
            "address": "רחוב אחר 45",
            "phone": "0527654321"
        }
        res = await client.put(f"/clients/{client_id}", json=update_data, headers=headers)
        assert res.status_code == 200
        assert res.json()["name"] == update_data["name"]

        res = await client.delete(f"/clients/{client_id}", headers=headers)
        assert res.status_code == 200

        res = await client.get(f"/clients/{client_id}", headers=headers)
        assert res.status_code == 404

@pytest.mark.asyncio
async def test_create_client_missing_required_fields():
    headers = await register_and_login()
    async with AsyncClient(base_url=CLIENTS_URL) as client:
        bad_data = {
            "email": "bad@example.com",
            "address": "רחוב כלשהו",
            "phone": "0500000000"
        }
        res = await client.post("/clients/", json=bad_data, headers=headers)
        assert res.status_code == 422

@pytest.mark.asyncio
async def test_unauthorized_access():
    async with AsyncClient(base_url=CLIENTS_URL) as client:
        res = await client.get("/clients/")
        assert res.status_code == 401
        res = await client.post("/clients/", json={"name": "NoAuth"})
        assert res.status_code == 401

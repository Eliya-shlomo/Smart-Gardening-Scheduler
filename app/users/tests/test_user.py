import pytest
from httpx import AsyncClient

USERS_URL = "http://localhost:8001"
CLIENTS_URL = "http://localhost:8002"
AUDIT_URL = "http://localhost:8003"

@pytest.mark.asyncio
async def register_and_login(email="test@example.com", password="12345678"):
    async with AsyncClient(base_url=USERS_URL) as client:
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


@pytest.mark.asyncio
async def test_create_get_update_client():
    headers = await register_and_login()
    create_data = {
        "name": "לקוח בדיקה",
        "email": "client@example.com",
        "address": "רחוב הבדיקה 12",
        "phone": "0501234567"
    }

    async with AsyncClient(base_url=CLIENTS_URL) as client:
        res = await client.post("/clients/", json=create_data, headers=headers)
        assert res.status_code == 200, f"Failed to create client: {res.text}"
        data = res.json()
        assert data["name"] == create_data["name"]
        assert data["email"] == create_data["email"]
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

@pytest.mark.asyncio
async def test_create_client_missing_fields():
    headers = await register_and_login()
    bad_data = {
        "email": "bad@example.com",
        "address": "רחוב כלשהו",
        "phone": "0500000000"
    }
    async with AsyncClient(base_url=CLIENTS_URL) as client:
        res = await client.post("/clients/", json=bad_data, headers=headers)
        assert res.status_code == 422, f"Expected 422 for missing fields, got {res.status_code} ({res.text})"

@pytest.mark.asyncio
async def test_audit_log_on_create_client():
    email = "uniqueuser@example.com"
    password = "UniquePassword123"
    headers = await register_and_login(email=email, password=password)

    create_data = {
        "name": "לקוח בדיקה לאודיט",
        "email": "auditclient@example.com",
        "address": "רחוב הלוג 1",
        "phone": "0512345678"
    }

    async with AsyncClient(base_url=CLIENTS_URL) as client:
        res = await client.post("/clients/", json=create_data, headers=headers)
        assert res.status_code == 200, f"Failed to create client: {res.text}"

    async with AsyncClient(base_url=AUDIT_URL) as audit_client:
        res = await audit_client.get("/audit_log/", params={"user_id": 1}, headers=headers)
        assert res.status_code == 200, f"Failed to get audit logs: {res.text}"
        logs = res.json()
        assert any(log["action"] == "create" for log in logs), "No create_client log found"


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
        login_data = {"email": email, "password": password}
        res = await client.post("/users/login", json=login_data)
        assert res.status_code == 200
        token = res.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}

@pytest.mark.asyncio
async def test_create_get_update_delete_client():
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
        client_id = res.json()["id"]

        res = await client.get(f"/clients/{client_id}", headers=headers)
        assert res.status_code == 200
        assert res.json()["email"] == create_data["email"]

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
        assert res.json()["detail"] == "Client deleted"

        res = await client.get(f"/clients/{client_id}", headers=headers)
        assert res.status_code == 404

@pytest.mark.asyncio
async def test_create_client_missing_required_fields():
    headers = await register_and_login(email="missingfields@example.com")
    bad_data = {
        "email": "bad@example.com",
        "address": "רחוב כלשהו",
        "phone": "0500000000"
    }
    async with AsyncClient(base_url=CLIENTS_URL) as client:
        res = await client.post("/clients/", json=bad_data, headers=headers)
        assert res.status_code == 422

@pytest.mark.asyncio
async def test_create_client_invalid_phone_and_name():
    headers = await register_and_login(email="invalidfields@example.com")
    async with AsyncClient(base_url=CLIENTS_URL) as client:
        bad_data_phone = {
            "name": "שם תקין",
            "email": "test2@example.com",
            "address": "כתובת תקינה",
            "phone": "05012abc"
        }
        res = await client.post("/clients/", json=bad_data_phone, headers=headers)
        assert res.status_code == 422

        bad_data_name = {
            "name": "Invalid@@!!",
            "email": "test3@example.com",
            "address": "כתובת תקינה",
            "phone": "0501234567"
        }
        res = await client.post("/clients/", json=bad_data_name, headers=headers)
        assert res.status_code == 422

@pytest.mark.asyncio
async def test_access_client_of_other_user():
    headers_user1 = await register_and_login(email="user1@example.com")
    async with AsyncClient(base_url=CLIENTS_URL) as client:
        create_data = {
            "name": "לקוח פרטי",
            "email": "privateclient@example.com",
            "address": "רחוב סודי 10",
            "phone": "0501234567"
        }
        res = await client.post("/clients/", json=create_data, headers=headers_user1)
        assert res.status_code == 200
        client_id = res.json()["id"]

    headers_user2 = await register_and_login(email="user2@example.com")
    async with AsyncClient(base_url=CLIENTS_URL) as client:
        res = await client.get(f"/clients/{client_id}", headers=headers_user2)
        assert res.status_code == 404
        update_data = {
            "name": "שינוי לא מורשה",
            "email": "hacker@example.com",
            "address": "רחוב אחר",
            "phone": "0500000000"
        }
        res = await client.put(f"/clients/{client_id}", json=update_data, headers=headers_user2)
        assert res.status_code == 404
        res = await client.delete(f"/clients/{client_id}", headers=headers_user2)
        assert res.status_code == 404

@pytest.mark.asyncio
async def test_unauthorized_access():
    async with AsyncClient(base_url=CLIENTS_URL) as client:
        res = await client.get("/clients/")
        assert res.status_code == 401
        res = await client.post("/clients/", json={"name": "NoAuth"})
        assert res.status_code == 401

@pytest.mark.asyncio
async def test_audit_log_on_create_client():
    email = "audittestuser@example.com"
    headers = await register_and_login(email=email)
    create_data = {
        "name": "לקוח בדיקה לאודיט",
        "email": "auditclient@example.com",
        "address": "רחוב הלוג 1",
        "phone": "0512345678"
    }
    async with AsyncClient(base_url=CLIENTS_URL) as client:
        res = await client.post("/clients/", json=create_data, headers=headers)
        assert res.status_code == 200
    async with AsyncClient(base_url=AUDIT_URL) as audit_client:
        res = await audit_client.get("/audit_log/", params={"user_id": 1}, headers=headers)
        assert res.status_code == 200, f"Failed to get audit logs: {res.text}"
        logs = res.json()
        assert any(log["action"] in ["create", "create_client"] for log in logs), "No create_client log found"

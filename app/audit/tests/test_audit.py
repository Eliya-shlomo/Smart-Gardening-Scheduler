import pytest
from httpx import AsyncClient
import uuid

USERS_URL = "http://localhost:8001"
CLIENTS_URL = "http://localhost:8002"
AUDIT_URL = "http://localhost:8003"

def random_email(prefix):
    return f"{prefix}_{uuid.uuid4().hex[:8]}@test.com"

@pytest.mark.asyncio
async def register_and_login(email=None, password="Testpass1"):
    if not email:
        email = random_email("audituser")
    async with AsyncClient(base_url=USERS_URL) as client:
        reg_res = await client.post("/users/register", json={
            "email": email,
            "password": password,
            "name": "AuditUser",   # תקני לפי רג'קס!
            "phone": "0501234567"
        })
        assert reg_res.status_code == 200, f"Register failed: {reg_res.text}"
        user_id = reg_res.json().get("user", {}).get("id") or reg_res.json().get("id")
        login_res = await client.post("/users/login", json={
            "email": email,
            "password": password
        })
        assert login_res.status_code == 200
        token = login_res.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}, user_id

@pytest.mark.asyncio
async def test_create_client_and_audit_log():
    headers, user_id = await register_and_login(email=random_email("create"))
    client_data = {
        "name": "לקוחבדיקה",   # תקני! (בלי תווים לא חוקיים)
        "email": random_email("client"),
        "address": "רחובבדיקה12",
        "phone": "0501234567"
    }
    async with AsyncClient(base_url=CLIENTS_URL) as client:
        res = await client.post("/clients/", json=client_data, headers=headers)
        assert res.status_code == 200, res.text
        client_id = res.json()["id"]

    async with AsyncClient(base_url=AUDIT_URL) as client:
        res = await client.get("/audit_log/", params={"user_id": user_id})
        logs = res.json()
        assert any(
            l["action"] in ["create", "create_client"] and l["entity_type"].lower() in ["client", "clients"] and l.get("entity_id") == client_id
            for l in logs
        ), "No create client log found in audit log!"

@pytest.mark.asyncio
async def test_update_client_and_audit_log():
    headers, user_id = await register_and_login(email=random_email("update"))
    client_data = {
        "name": "לקוחעדכון",
        "email": random_email("updateclient"),
        "address": "רחובעדכון10",
        "phone": "0509876543"
    }
    async with AsyncClient(base_url=CLIENTS_URL) as client:
        res = await client.post("/clients/", json=client_data, headers=headers)
        assert res.status_code == 200
        client_id = res.json()["id"]

        update_data = {
            "name": "לקוחעודכן",
            "email": client_data["email"],
            "address": "רחובחדש100",
            "phone": "0501111111"
        }
        res = await client.put(f"/clients/{client_id}", json=update_data, headers=headers)
        assert res.status_code == 200

    async with AsyncClient(base_url=AUDIT_URL) as client:
        res = await client.get("/audit_log/", params={"user_id": user_id})
        logs = res.json()
        assert any(
            l["action"] in ["update", "update_client"] and l["entity_type"].lower() in ["client", "clients"] and l.get("entity_id") == client_id
            for l in logs
        ), "No update client log found in audit log!"

@pytest.mark.asyncio
async def test_delete_client_and_audit_log():
    headers, user_id = await register_and_login(email=random_email("delete"))
    client_data = {
        "name": "לקוחמחיקה",
        "email": random_email("deleteclient"),
        "address": "רחובמחיקה33",
        "phone": "0522222222"
    }
    async with AsyncClient(base_url=CLIENTS_URL) as client:
        res = await client.post("/clients/", json=client_data, headers=headers)
        assert res.status_code == 200
        client_id = res.json()["id"]

        res = await client.delete(f"/clients/{client_id}", headers=headers)
        assert res.status_code == 200

    async with AsyncClient(base_url=AUDIT_URL) as client:
        res = await client.get("/audit_log/", params={"user_id": user_id})
        logs = res.json()
        assert any(
            l["action"] in ["delete", "delete_client"] and l["entity_type"].lower() in ["client", "clients"] and l.get("entity_id") == client_id
            for l in logs
        ), "No delete client log found in audit log!"

@pytest.mark.asyncio
async def test_user_registration_logs_to_audit():
    email = random_email("register")
    password = "Testpass1"
    async with AsyncClient(base_url=USERS_URL) as client:
        reg_res = await client.post("/users/register", json={
            "email": email,
            "password": password,
            "name": "AuditUser2",    # תקין!
            "phone": "0500000004"
        })
        assert reg_res.status_code == 200, reg_res.text
        user_id = reg_res.json().get("user", {}).get("id") or reg_res.json().get("id")
    async with AsyncClient(base_url=AUDIT_URL) as client:
        res = await client.get("/audit_log/", params={"user_id": user_id})
        logs = res.json()
        assert any(
            l["action"] in ["register", "create", "register_user"] and l["entity_type"].lower() in ["user", "users"]
            for l in logs
        ), "No registration log found for user in audit log!"

@pytest.mark.asyncio
async def test_audit_log_access_without_user_id():
    async with AsyncClient(base_url=AUDIT_URL) as client:
        res = await client.get("/audit_log/")
        assert res.status_code in [422, 400]  # missing user_id param

@pytest.mark.asyncio
async def test_audit_log_create_without_required_fields():
    async with AsyncClient(base_url=AUDIT_URL) as client:
        bad_payload = {
            "user_id": 12345,
        }
        res = await client.post("/audit_log/", json=bad_payload)
        assert res.status_code == 422  # validation error

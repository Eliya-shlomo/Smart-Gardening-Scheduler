import pytest
from httpx import AsyncClient
import uuid

import pytest
from httpx import AsyncClient
import uuid

USERS_URL = "http://localhost:8001"
CLIENTS_URL = "http://localhost:8002"
APPOINTMENTS_URL = "http://localhost:8004"

def random_email(prefix):
    return f"{prefix}_{uuid.uuid4().hex[:8]}@test.com"

@pytest.mark.asyncio
async def register_and_login(email=None, password="Testpass1"):
    if not email:
        email = random_email("apuser")
    async with AsyncClient(base_url=USERS_URL) as client:
        reg_res = await client.post("/users/register", json={
            "email": email,
            "password": password,
            "name": "AppointmentUser",
            "phone": "0501111222"
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
async def create_client(headers):
    async with AsyncClient(base_url=CLIENTS_URL) as client:
        client_data = {
            "name": "לקוחבדיקה",
            "email": random_email("client"),
            "address": "תל אביב 5",
            "phone": "0501111111"
        }
        res = await client.post("/clients/", json=client_data, headers=headers)
        assert res.status_code == 200, f"Create client failed: {res.text}"
        return res.json()["id"]

@pytest.mark.asyncio
async def test_create_and_get_appointment():
    headers, user_id = await register_and_login()
    client_id = await create_client(headers)
    appointment_data = {
        "client_id": client_id,
        "date": "2025-08-01T09:00:00",
        "time": "09:00", 
        "status": "pending",
        "notes": "בדיקת E2E",
        "treatment_type": "הדברה"
    }
    async with AsyncClient(base_url=APPOINTMENTS_URL) as client:
        res = await client.post("/appointments/", json=appointment_data, headers=headers)
        assert res.status_code == 200, res.text
        appointment = res.json()
        assert appointment["client_id"] == client_id
        assert appointment["status"] == "pending"
        appointment_id = appointment["id"]

        res = await client.get(f"/appointments/client/{client_id}", headers=headers)
        assert res.status_code == 200
        appointments = res.json()
        assert any(a["id"] == appointment_id for a in appointments)

@pytest.mark.asyncio
async def test_update_and_patch_appointment():
    headers, user_id = await register_and_login()
    client_id = await create_client(headers)
    async with AsyncClient(base_url=APPOINTMENTS_URL) as client:
        res = await client.post("/appointments/", json={

            "client_id": client_id,
            "date": "2025-08-01T12:00:00",
            "time": "09:00",  
            "status": "pending",
            "notes": "עדכון",
            "treatment_type": "השקיה"
        }, headers=headers)
        assert res.status_code == 200
        appointment_id = res.json()["id"]

        # עדכון מלא
        update_data = {
            "client_id": client_id,
            "date": "2025-08-01T13:00:00",
            "time": "09:00",  
            "status": "pending",
            "notes": "עודכן",
            "treatment_type": "גיזום"
        }
        res = await client.put(f"/appointments/{appointment_id}", json=update_data, headers=headers)
        assert res.status_code == 200
        assert res.json()["notes"] == "עודכן"
        assert res.json()["treatment_type"] == "גיזום"

        # עדכון סטטוס בלבד (PATCH)
        patch_data = {"status": "done"}
        res = await client.patch(f"/appointments/{appointment_id}", json=patch_data, headers=headers)
        assert res.status_code == 200
        assert res.json()["status"] == "done"

@pytest.mark.asyncio
async def test_delete_appointment():
    headers, user_id = await register_and_login()
    client_id = await create_client(headers)
    async with AsyncClient(base_url=APPOINTMENTS_URL) as client:
        res = await client.post("/appointments/", json={
            "client_id": client_id,
            "date": "2025-08-02T10:00:00",
            "time": "09:00",  
            "status": "pending",
            "notes": "למחיקה",
            "treatment_type": "דישון"
        }, headers=headers)
        assert res.status_code == 200
        appointment_id = res.json()["id"]

        res = await client.delete(f"/appointments/{appointment_id}", headers=headers)
        assert res.status_code == 200

        res = await client.put(f"/appointments/{appointment_id}", json={
            "client_id": client_id,
            "date": "2025-08-02T10:00:00",
            "time": "09:00",  
            "status": "pending",
            "notes": "למחיקה",
            "treatment_type": "דישון"
        }, headers=headers)
        assert res.status_code in (403, 404)

@pytest.mark.asyncio
async def test_appointment_missing_fields():
    headers, user_id = await register_and_login()
    async with AsyncClient(base_url=APPOINTMENTS_URL) as client:
        bad_data = {
            "date": "2025-08-05T10:00:00",
            "status": "pending",
            "notes": "חסר client_id",
            "treatment_type": "ריסוס"
        }
        res = await client.post("/appointments/", json=bad_data, headers=headers)
        assert res.status_code == 422

@pytest.mark.asyncio
async def test_appointment_unauthorized_access():
    async with AsyncClient(base_url=APPOINTMENTS_URL) as client:
        res = await client.post("/appointments/", json={
            "client_id": 1,
            "date": "2025-08-07T10:00:00",
            "time": "09:00",  
            "status": "pending",
            "notes": "ללא טוקן",
            "treatment_type": "דישון"
        })
        assert res.status_code in (401, 403)

@pytest.mark.asyncio
async def test_access_appointment_of_other_user():
    # יוזר 1
    headers1, user_id1 = await register_and_login(email=random_email("user1"))
    client_id1 = await create_client(headers1)
    # יוזר 2
    headers2, user_id2 = await register_and_login(email=random_email("user2"))
    client_id2 = await create_client(headers2)

    async with AsyncClient(base_url=APPOINTMENTS_URL) as client:
        res = await client.post("/appointments/", json={
            "client_id": client_id1,
            "date": "2025-08-10T12:00:00",
            "time": "09:00",  
            "status": "pending",
            "notes": "פרטי",
            "treatment_type": "השקיה"
        }, headers=headers1)
        assert res.status_code == 200
        appointment_id = res.json()["id"]

        res = await client.get(f"/appointments/client/{client_id1}", headers=headers2)
        assert res.status_code == 403

        patch_data = {"status": "done"}
        res = await client.patch(f"/appointments/{appointment_id}", json=patch_data, headers=headers2)
        assert res.status_code == 403

        res = await client.delete(f"/appointments/{appointment_id}", headers=headers2)
        assert res.status_code == 403

@pytest.mark.asyncio
async def test_appointment_invalid_client():
    headers, user_id = await register_and_login()
    bad_client_id = 99999999
    async with AsyncClient(base_url=APPOINTMENTS_URL) as client:
        res = await client.post("/appointments/", json={
            "client_id": bad_client_id,
            "date": "2025-08-10T12:00:00",
            "time": "09:00",  
            "status": "pending",
            "notes": "לקוח לא קיים",
            "treatment_type": "בדיקה"
        }, headers=headers)
        assert res.status_code in (403, 404)

import pytest
import uuid

@pytest.mark.asyncio
async def test_create_appointment(client):
    await client.post("/users/register", json={
        "email": "appt@test.com",
        "password": "12345678",
        "name": "Appt Tester",
        "phone": "0501234567"
    })

    login = await client.post("/users/login", json={
        "email": "appt@test.com",
        "password": "12345678"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # יצירת אימייל ייחודי
    email = f"client_{uuid.uuid4().hex[:6]}@example.com"

    client_res = await client.post(
        "/clients/",
        json={"name": "Appointment Client", "email": email, "address": "Beer Sheva", "phone": "0500000000"},
        headers=headers
    )
    assert client_res.status_code == 200, f"Client creation failed: {client_res.text}"
    client_id = client_res.json()["id"]

    res = await client.post(
        "/appointments/",
        json={
            "client_id": client_id,
            "date": "2025-07-10T09:00:00",
            "time": "09:00",
            "treatment_type": "בדיקת עונתית",
            "notes": "Seasonal Check"
        },
        headers=headers
    )
    assert res.status_code == 200, f"Appointment creation failed: {res.text}"

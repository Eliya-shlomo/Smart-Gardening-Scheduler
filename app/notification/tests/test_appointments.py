import pytest
import uuid
from datetime import datetime, timedelta

# This test creates a user, logs in, creates a client, and then creates an appointment.
# It checks that the appointment is created successfully and returned with correct client_id.
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
            "date": (datetime.now() + timedelta(days=1)).isoformat(),
            "time": "09:00",
            "treatment_type": "בדיקת עונתית",
            "notes": "Seasonal Check"
        },
        headers=headers
    )
    assert res.status_code == 200, f"Appointment creation failed: {res.text}"
    assert res.json()["client_id"] == client_id


# This test tries to create an appointment for a client that doesn't exist -> should fail 
@pytest.mark.asyncio
async def test_create_appointment_invalid_client(client):
    await client.post("/users/register", json={
        "email": "appt2@test.com",
        "password": "12345678",
        "name": "Invalid Client",
        "phone": "0501234567"
    })
    login = await client.post("/users/login", json={
        "email": "appt2@test.com",
        "password": "12345678"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = await client.post("/appointments/", json={
        "client_id": 999999,
        "date": datetime.now().isoformat(),
        "time": "10:00",
        "treatment_type": "Invalid",
        "notes": "N/A"
    }, headers=headers)
    assert res.status_code in (403, 404, 422)


# This test updates an existing appointment's status and notes.
# It verifies that the update is saved and returned correctly.
@pytest.mark.asyncio
async def test_update_appointment_status(client):
    await client.post("/users/register", json={
        "email": "appt3@test.com",
        "password": "12345678",
        "name": "Update Tester",
        "phone": "0501234567"
    })
    login = await client.post("/users/login", json={
        "email": "appt3@test.com",
        "password": "12345678"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    email = f"client_{uuid.uuid4().hex[:6]}@example.com"
    client_res = await client.post("/clients/", json={
        "name": "Client Update",
        "email": email,
        "address": "Somewhere",
        "phone": "0501231234"
    }, headers=headers)
    client_id = client_res.json()["id"]

    appt_res = await client.post("/appointments/", json={
        "client_id": client_id,
        "date": datetime.now().isoformat(),
        "time": "11:00",
        "treatment_type": "Update Test",
        "notes": "Initial"
    }, headers=headers)
    appointment_id = appt_res.json()["id"]

    update_res = await client.patch(f"/appointments/{appointment_id}", json={
        "status": "done",
        "notes": "Completed successfully"
    }, headers=headers)
    assert update_res.status_code == 200
    assert update_res.json()["status"] == "done"
    assert update_res.json()["notes"] == "Completed successfully"


# This test deletes an appointment and confirms it no longer exists.
@pytest.mark.asyncio
async def test_delete_appointment(client):
    await client.post("/users/register", json={
        "email": "appt4@test.com",
        "password": "12345678",
        "name": "Delete Tester",
        "phone": "0501234567"
    })
    login = await client.post("/users/login", json={
        "email": "appt4@test.com",
        "password": "12345678"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    email = f"client_{uuid.uuid4().hex[:6]}@example.com"
    client_res = await client.post("/clients/", json={
        "name": "Client Delete",
        "email": email,
        "address": "City",
        "phone": "0509999999"
    }, headers=headers)
    client_id = client_res.json()["id"]

    appt_res = await client.post("/appointments/", json={
        "client_id": client_id,
        "date": datetime.now().isoformat(),
        "time": "12:00",
        "treatment_type": "To Delete",
        "notes": "Not Applicable"
    }, headers=headers)
    print("Create appointment response:", appt_res.status_code, appt_res.text)

    appointment_id = appt_res.json()["id"]


    del_res = await client.delete(f"/appointments/{appointment_id}", headers=headers)
    assert del_res.status_code == 200

    get_res = await client.get(f"/appointments/client/{client_id}", headers=headers)
    assert appointment_id not in [appt["id"] for appt in get_res.json()]


# This test checks that accessing appointments without a token is blocked.
@pytest.mark.asyncio
async def test_get_appointments_unauthorized(client):
    res = await client.get("/appointments/client/1")
    assert res.status_code == 401


# This test tries to update an appointment that doesn't belong to the user -> should fail
@pytest.mark.asyncio
async def test_update_unauthorized_appointment(client):
    await client.post("/users/register", json={
        "email": "appt5@test.com",
        "password": "12345678",
        "name": "Unauthorized",
        "phone": "0501234567"
    })
    login = await client.post("/users/login", json={
        "email": "appt5@test.com",
        "password": "12345678"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = await client.patch("/appointments/999999", json={
        "status": "done",
        "notes": "Invalid update"
    }, headers=headers)
    assert res.status_code in (403, 404)


# This test tries to create an appointment with invalid time format -> Should return error (422)
@pytest.mark.asyncio
async def test_create_appointment_invalid_time_format(client):
    await client.post("/users/register", json={
        "email": "appt6@test.com",
        "password": "12345678",
        "name": "Time Format Tester",
        "phone": "0501234567"
    })
    login = await client.post("/users/login", json={
        "email": "appt6@test.com",
        "password": "12345678"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    email = f"client_{uuid.uuid4().hex[:6]}@example.com"
    client_res = await client.post("/clients/", json={
        "name": "Time Format Client",
        "email": email,
        "address": "Testville",
        "phone": "0500000000"
    }, headers=headers)
    client_id = client_res.json()["id"]

    res = await client.post("/appointments/", json={
        "client_id": client_id,
        "date": datetime.now().isoformat(),
        "time": "invalid",
        "treatment_type": "Test",
        "notes": "Wrong time"
    }, headers=headers)
    assert res.status_code == 422

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
async def test_create_get_update_delete_client(client):
    headers = await register_and_login(client)

    # Creating a valid client
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
    client_id = data["id"]

    # Accepting the client we created
    res = await client.get(f"/clients/{client_id}", headers=headers)
    assert res.status_code == 200
    assert res.json()["email"] == create_data["email"]

    # Update the client with valid fields
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

    # Deleting the client
    res = await client.delete(f"/clients/{client_id}", headers=headers)
    assert res.status_code == 200
    assert res.json()["detail"] == "Client deleted"

# Attempting to receive a customer after deletion - should get a 404
    res = await client.get(f"/clients/{client_id}", headers=headers)
    assert res.status_code == 404

@pytest.mark.asyncio
async def test_create_client_missing_required_fields(client):
    headers = await register_and_login(client)

    #Missing name (required field)
    bad_data = {
        "email": "bad@example.com",
        "address": "רחוב כלשהו",
        "phone": "0500000000"
    }
    res = await client.post("/clients/", json=bad_data, headers=headers)
    assert res.status_code == 422

@pytest.mark.asyncio
async def test_create_client_invalid_phone_and_name(client):
    headers = await register_and_login(client)

    # Phone with invalid characters
    bad_data_phone = {
        "name": "שם תקין",
        "email": "test2@example.com",
        "address": "כתובת תקינה",
        "phone": "05012abc"  # לא חוקי
    }
    res = await client.post("/clients/", json=bad_data_phone, headers=headers)
    assert res.status_code == 422

    # Name with invalid characters (including special characters)
    bad_data_name = {
        "name": "Invalid@@!!",
        "email": "test3@example.com",
        "address": "כתובת תקינה",
        "phone": "0501234567"
    }
    res = await client.post("/clients/", json=bad_data_name, headers=headers)
    assert res.status_code == 422

@pytest.mark.asyncio
async def test_access_client_of_other_user(client):
    # user 1
    headers_user1 = await register_and_login(client, email="user1@example.com")

    create_data = {
        "name": "לקוח פרטי",
        "email": "privateclient@example.com",
        "address": "רחוב סודי 10",
        "phone": "0501234567"
    }
    res = await client.post("/clients/", json=create_data, headers=headers_user1)
    assert res.status_code == 200
    client_id = res.json()["id"]

    # user 1
    headers_user2 = await register_and_login(client, email="user2@example.com")

# User 2 tries to access User 1's client - should get 404 (or Forbidden)
    res = await client.get(f"/clients/{client_id}", headers=headers_user2)
    assert res.status_code == 404

# User 2 tries to update user 1's client
    update_data = {
        "name": "שינוי לא מורשה",
        "email": "hacker@example.com",
        "address": "רחוב אחר",
        "phone": "0500000000"
    }
    res = await client.put(f"/clients/{client_id}", json=update_data, headers=headers_user2)
    assert res.status_code == 404

# User 2 tries to delete user 1's client
    res = await client.delete(f"/clients/{client_id}", headers=headers_user2)
    assert res.status_code == 404


@pytest.mark.asyncio
async def test_unauthorized_access(client):
    # ניסיון לקבל את רשימת הלקוחות ללא token
    res = await client.get("/clients/")
    assert res.status_code == 401

    # ניסיון ליצור לקוח ללא token
    res = await client.post("/clients/", json={"name": "NoAuth"})
    assert res.status_code == 401

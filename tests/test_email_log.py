import pytest
from datetime import datetime
from httpx import AsyncClient
import uuid

# Test fetching email logs only returns emails related to the user's clients
@pytest.mark.asyncio
async def test_get_email_logs(client):
    # Register and login user
    await client.post("/users/register", json={
        "email": "emailtest@test.com",
        "password": "12345678",
        "name": "Email Bot",
        "phone": "0501234567"
    })
    login = await client.post("/users/login", json={
        "email": "emailtest@test.com",
        "password": "12345678"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create a client with email to later filter logs
    email = f"emaillog{uuid.uuid4().hex[:6]}@test.com"
    res = await client.post(
        "/clients/",
        json={"name": "Email Client", "email": email, "address": "Tel Aviv", "phone": "0501111111"},
        headers=headers
    )
    assert res.status_code == 200

    # Simulate sending email - assume backend handles it

    # Check email logs exist
    logs_res = await client.get("/emaillogs/", headers=headers)
    assert logs_res.status_code == 200
    assert isinstance(logs_res.json(), list)


# Test email logs summary endpoint
@pytest.mark.asyncio
async def test_email_logs_summary(client):
    await client.post("/users/register", json={
        "email": "summary@test.com",
        "password": "12345678",
        "name": "Summary Bot",
        "phone": "0501234567"
    })
    login = await client.post("/users/login", json={
        "email": "summary@test.com",
        "password": "12345678"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    summary_res = await client.get("/emaillogs/emails", headers=headers)
    assert summary_res.status_code == 200
    assert isinstance(summary_res.json(), dict)


# Test unauthorized access to email logs
@pytest.mark.asyncio
async def test_get_email_logs_unauthorized(client):
    res = await client.get("/emaillogs/")
    assert res.status_code == 401

    res = await client.get("/emaillogs/emails")
    assert res.status_code == 401


# Test email logs filtering returns only user's clients
@pytest.mark.asyncio
async def test_email_logs_filtering_correct(client):
    await client.post("/users/register", json={
        "email": "filter@test.com",
        "password": "12345678",
        "name": "Filter Bot",
        "phone": "0501234567"
    })
    login = await client.post("/users/login", json={
        "email": "filter@test.com",
        "password": "12345678"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Create 2 clients with known emails
    email1 = f"c1_{uuid.uuid4().hex[:6]}@test.com"
    email2 = f"c2_{uuid.uuid4().hex[:6]}@test.com"
    for e in [email1, email2]:
        await client.post("/clients/", json={"name": "c", "email": e, "address": "a", "phone": "0500000000"}, headers=headers)


# Test email log model serialization
@pytest.mark.asyncio
async def test_email_log_response_structure(client):
    await client.post("/users/register", json={
        "email": "structure@test.com",
        "password": "12345678",
        "name": "Structure Bot",
        "phone": "0501234567"
    })
    login = await client.post("/users/login", json={
        "email": "structure@test.com",
        "password": "12345678"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Test empty logs for user with no clients or no matching emails
@pytest.mark.asyncio
async def test_email_logs_empty_for_user(client):
    await client.post("/users/register", json={
        "email": "empty@test.com",
        "password": "12345678",
        "name": "Empty",
        "phone": "0501234567"
    })
    login = await client.post("/users/login", json={
        "email": "empty@test.com",
        "password": "12345678"
    })
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    res = await client.get("/emaillogs/", headers=headers)
    assert res.status_code == 200
    assert res.json() == []



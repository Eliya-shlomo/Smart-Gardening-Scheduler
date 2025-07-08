import pytest
from httpx import AsyncClient, ASGITransport
from datetime import datetime
from backend.main import app

@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac

async def register_and_login(client, email="tree@test.com", password="12345678"):
    await client.post("/users/register", json={
        "email": email,
        "password": password,
        "name": "Tree Owner",
        "phone": "0501234567"
    })

    login = await client.post("/users/login", json={
        "email": email,
        "password": password
    })
    return login.json()["access_token"]

async def create_client(client, headers):
    res = await client.post(
        "/clients/",
        json={
            "name": "Client 1",
            "email": "client1@example.com",
            "address": "Tel Aviv",
            "phone": "0500000000"
        },
        headers=headers
    )
    return res.json()["id"]

@pytest.mark.asyncio
async def test_create_and_get_tree(client):
    token = await register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}
    client_id = await create_client(client, headers)

    res = await client.post("/trees/", json={
        "type": "Mango",
        "planting_date": datetime.now().isoformat(),
        "notes": "Healthy tree",
        "client_id": client_id
    }, headers=headers)
    assert res.status_code == 200, f"Update failed: {res.text}"
    tree_id = res.json()["id"]

    res = await client.get(f"/trees/client/{client_id}", headers=headers)
    assert res.status_code == 200
    assert any(t["id"] == tree_id and t["type"] == "Mango" for t in res.json())

@pytest.mark.asyncio
async def test_update_tree(client):
    token = await register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}
    client_id = await create_client(client, headers)

    res = await client.post("/trees/", json={
        "type": "Olive",
        "notes": "צעיר",
        "client_id": client_id
    }, headers=headers)
    tree_id = res.json()["id"]

    res = await client.put(f"/trees/{tree_id}", json={
        "type": "Updated Olive",
        "planting_date": datetime.now().isoformat(),
        "notes": "מעודכן"
    }, headers=headers)
    assert res.status_code == 200, f"Update failed: {res.text}"
    updated = res.json()
    assert updated["type"] == "Updated Olive"
    assert updated["notes"] == "מעודכן"
    assert res.status_code == 200, f"Failed: {res.text}"


@pytest.mark.asyncio
async def test_delete_tree(client):
    token = await register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}
    client_id = await create_client(client, headers)

    res = await client.post("/trees/", json={
        "type": "Lemon",
        "client_id": client_id
    }, headers=headers)
    tree_id = res.json()["id"]

    res = await client.delete(f"/trees/{tree_id}", headers=headers)
    assert res.status_code == 200

    res = await client.get(f"/trees/client/{client_id}", headers=headers)
    assert all(t["id"] != tree_id for t in res.json())

@pytest.mark.asyncio
async def test_create_tree_invalid_client(client):
    token = await register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    res = await client.post("/trees/", json={
        "type": "Fake",
        "client_id": 99999
    }, headers=headers)
    assert res.status_code in (403, 404)

@pytest.mark.asyncio
async def test_get_trees_unauthorized(client):
    res = await client.get("/trees/client/1")
    assert res.status_code == 401

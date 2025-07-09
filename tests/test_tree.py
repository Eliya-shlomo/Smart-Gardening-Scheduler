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
    assert login.status_code == 200
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
    assert res.status_code == 200
    return res.json()["id"]


@pytest.mark.asyncio
async def test_create_and_get_tree(client):
    token = await register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}
    client_id = await create_client(client, headers)

# Create a new tree
    res = await client.post("/trees/", json={
        "type": "Mango",
        "planting_date": datetime.now().isoformat(),
        "notes": "Healthy tree",
        "client_id": client_id
    }, headers=headers)
    assert res.status_code == 200, f"Create failed: {res.text}"
    tree_id = res.json()["id"]

    # Retrieving trees for the customer and checking that the new tree exists
    res = await client.get(f"/trees/client/{client_id}", headers=headers)
    assert res.status_code == 200
    trees = res.json()
    assert any(t["id"] == tree_id and t["type"] == "Mango" for t in trees)

@pytest.mark.asyncio
async def test_update_tree(client):
    token = await register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}
    client_id = await create_client(client, headers)

    # Create a tree
    res = await client.post("/trees/", json={
        "type": "Olive",
        "notes": "צעיר",
        "client_id": client_id
    }, headers=headers)
    assert res.status_code == 200
    tree_id = res.json()["id"]

    # Update the tree
    update_payload = {
        "type": "Updated Olive",
        "planting_date": datetime.now().isoformat(),
        "notes": "מעודכן"
    }
    res = await client.put(f"/trees/{tree_id}", json=update_payload, headers=headers)
    assert res.status_code == 200, f"Update failed: {res.text}"
    updated = res.json()
    assert updated["type"] == update_payload["type"]
    assert updated["notes"] == update_payload["notes"]

@pytest.mark.asyncio
async def test_delete_tree(client):
    token = await register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}
    client_id = await create_client(client, headers)

    # Create a tree
    res = await client.post("/trees/", json={
        "type": "Lemon",
        "client_id": client_id
    }, headers=headers)
    assert res.status_code == 200
    tree_id = res.json()["id"]

    # Delete the tree
    res = await client.delete(f"/trees/{tree_id}", headers=headers)
    assert res.status_code == 200

    # Check that the tree is no longer found
    res = await client.get(f"/trees/client/{client_id}", headers=headers)
    assert res.status_code == 200
    assert all(t["id"] != tree_id for t in res.json())

@pytest.mark.asyncio
async def test_create_tree_invalid_client(client):
    token = await register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Attempt to create a tree for a non-existent client
    res = await client.post("/trees/", json={
        "type": "Fake",
        "client_id": 99999
    }, headers=headers)
    assert res.status_code in (403, 404)

@pytest.mark.asyncio
async def test_get_trees_unauthorized(client):
    # Attempt access without a token
    res = await client.get("/trees/client/1")
    assert res.status_code == 401

@pytest.mark.asyncio
async def test_create_tree_invalid_data(client):
    token = await register_and_login(client)
    headers = {"Authorization": f"Bearer {token}"}
    client_id = await create_client(client, headers)

    # Attempt to create a tree with an invalid name
    res = await client.post("/trees/", json={
        "type": "!!@@##$$",  
        "client_id": client_id
    }, headers=headers)
    assert res.status_code == 422

@pytest.mark.asyncio
async def test_update_tree_unauthorized_access(client):
    token1 = await register_and_login(client, email="user1@example.com")
    headers1 = {"Authorization": f"Bearer {token1}"}
    client_id = await create_client(client, headers1)

    # User 1 creates a tree
    res = await client.post("/trees/", json={
        "type": "Pine",
        "client_id": client_id
    }, headers=headers1)
    tree_id = res.json()["id"]

    # User 2 registered
    token2 = await register_and_login(client, email="user2@example.com")
    headers2 = {"Authorization": f"Bearer {token2}"}

   # User 2 tries to update user 1's tree -> should fail
    update_payload = {
        "type": "Hacked Pine",
        "planting_date": datetime.now().isoformat(),
        "notes": "Not allowed"
    }
    res = await client.put(f"/trees/{tree_id}", json=update_payload, headers=headers2)
    assert res.status_code == 403

@pytest.mark.asyncio
async def test_delete_tree_unauthorized_access(client):
    token1 = await register_and_login(client, email="user3@example.com")
    headers1 = {"Authorization": f"Bearer {token1}"}
    client_id = await create_client(client, headers1)

    # User 1 creates a tree
    res = await client.post("/trees/", json={
        "type": "Apple",
        "client_id": client_id
    }, headers=headers1)
    tree_id = res.json()["id"]

    # User 2 registered
    token2 = await register_and_login(client, email="user4@example.com")
    headers2 = {"Authorization": f"Bearer {token2}"}

# User 2 tries to delete user 1's tree - should fail
    res = await client.delete(f"/trees/{tree_id}", headers=headers2)
    assert res.status_code == 403

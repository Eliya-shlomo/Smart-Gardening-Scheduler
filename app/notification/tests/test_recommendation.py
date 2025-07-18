import pytest
from httpx import AsyncClient
from fastapi import status
import uuid

USERS_URL = "http://localhost:8001/users"
NOTIFICATION_URL = "http://localhost:8007/notification"  

@pytest.fixture
async def user_token():
    async with AsyncClient(base_url=USERS_URL) as client:
        random_email = f"test_{uuid.uuid4().hex[:8]}@example.com"

        user_data = {
            "email": random_email,
            "name": "TestUser123",
            "phone": "0521234567",
            "password": "Password123!"
        }

        reg_resp = await client.post("/register", json=user_data)
        assert reg_resp.status_code == 200, f"Registration failed: {reg_resp.text}"

        resp = await client.post("/login", json={
            "email": user_data["email"],
            "password": user_data["password"]
        })

        assert resp.status_code == 200, f"Login failed: {resp.text}"
        token = resp.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}


@pytest.mark.asyncio
async def test_full_recommendation_flow(user_token):
    async with AsyncClient(base_url=NOTIFICATION_URL) as client:
        rec_payload = {
            "tree_id": 10,
            "type": "Watering",
            "notes": "Deep watering for summer"
        }

        create_resp = await client.post("/recommendation/", json=rec_payload, headers=user_token)
        assert create_resp.status_code == 200
        created_rec = create_resp.json()
        rec_id = created_rec["id"]
        assert created_rec["type"] == "Watering"

        dup_resp = await client.post("/recommendation/", json=rec_payload, headers=user_token)
        assert dup_resp.status_code == 400
        assert "already sent" in dup_resp.json()["detail"]

        all_resp = await client.get("/recommendation/", headers=user_token)
        assert all_resp.status_code == 200
        assert any(rec["id"] == rec_id for rec in all_resp.json())

        single_resp = await client.get(f"/recommendation/{rec_id}", headers=user_token)
        assert single_resp.status_code == 200
        assert single_resp.json()["tree_id"] == 10

        delete_resp = await client.delete(f"/recommendation/{rec_id}", headers=user_token)
        assert delete_resp.status_code == 200
        assert delete_resp.json()["id"] == rec_id

        get_deleted = await client.get(f"/recommendation/{rec_id}", headers=user_token)
        assert get_deleted.status_code == 404


@pytest.mark.asyncio
async def test_create_different_type_same_tree(user_token):
    async with AsyncClient(base_url=NOTIFICATION_URL) as client:
        payload1 = {
            "tree_id": 20,
            "type": "Pruning",
            "notes": "Winter cut"
        }
        payload2 = {
            "tree_id": 20,
            "type": "Fertilizing",
            "notes": "Apply compost"
        }

        res1 = await client.post("/recommendation/", json=payload1, headers=user_token)
        res2 = await client.post("/recommendation/", json=payload2, headers=user_token)

        assert res1.status_code == 200
        assert res2.status_code == 200


@pytest.mark.asyncio
async def test_unauthorized_access_rejected():
    async with AsyncClient(base_url=NOTIFICATION_URL) as client:
        payload = {
            "tree_id": 30,
            "type": "Watering",
            "notes": "Unauthorized attempt"
        }
        res = await client.post("/recommendation/", json=payload, headers={"Authorization": "Bearer invalidtoken123"})
        assert res.status_code == 401


@pytest.mark.asyncio
async def test_access_without_token():
    async with AsyncClient(base_url=NOTIFICATION_URL) as client:
        res = await client.get("/recommendation/")
        assert res.status_code == 401


@pytest.mark.asyncio
async def test_invalid_type_field(user_token):
    async with AsyncClient(base_url=NOTIFICATION_URL) as client:
        payload = {
            "tree_id": 40,
            "type": "!!!",  # לא עומד בפטרן
            "notes": "bad type"
        }

        res = await client.post("/recommendation/", json=payload, headers=user_token)
        assert res.status_code == 422


@pytest.mark.asyncio
async def test_optional_notes(user_token):
    async with AsyncClient(base_url=NOTIFICATION_URL) as client:
        payload = {
            "tree_id": 50,
            "type": "Watering"
            # notes חסר בכוונה
        }

        res = await client.post("/recommendation/", json=payload, headers=user_token)
        assert res.status_code == 200
        assert res.json()["notes"] is None

@pytest.mark.asyncio
async def test_delete_nonexistent_recommendation(user_token):
    async with AsyncClient(base_url=NOTIFICATION_URL) as client:
        res = await client.delete("/recommendation/999999", headers=user_token)
        assert res.status_code == 404

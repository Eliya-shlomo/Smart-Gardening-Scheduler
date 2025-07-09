import pytest
from httpx import AsyncClient, ASGITransport
from backend.main import app
from backend.database import get_db
from backend.models import AuditLog, User
from backend.crud.audit_log import create_log
from datetime import datetime

@pytest.fixture(scope="function", autouse=True)
def clean_db():
    db = next(get_db())
    try:
        # מחיקת כל רשומות ה-audit_logs קודם
        db.query(AuditLog).delete()
        db.commit()

        # עכשיו מחיקת המשתמשים
        db.query(User).delete()
        db.commit()
    except:
        db.rollback()
        raise
    finally:
        db.close()
    yield


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
async def test_get_my_logs_empty(client):
    headers = await register_and_login(client, email="emptylogs@test.com")

    res = await client.get("/audit-log/", headers=headers)
    assert res.status_code == 200
    assert isinstance(res.json(), list)
    assert len(res.json()) == 0  # No logs yet

@pytest.mark.asyncio
async def test_create_log_and_get_logs(client):
    headers = await register_and_login(client, email="logtest@test.com")
    
    # קבלת id של המשתמש שנוצר דרך ה-API
    user_res = await client.get("/users/me", headers=headers)
    assert user_res.status_code == 200
    user_id = user_res.json()["id"]

    # יצירת לוג דרך קריאה לסינכרון ב-threadpool כדי לא לחסום את הלולאה
    import asyncio
    from functools import partial
    db = next(get_db())
    await asyncio.get_running_loop().run_in_executor(
        None, partial(create_log, db, user_id, "create", "client", 123, "Created client 123")
    )

    res = await client.get("/audit-log/", headers=headers)
    assert res.status_code == 200
    logs = res.json()
    assert len(logs) > 0
    assert any(log["action"] == "create" and log["entity_id"] == 123 for log in logs)
    assert logs[0]["timestamp"]

@pytest.mark.asyncio
async def test_get_logs_limit(client):
    headers = await register_and_login(client, email="limitlogs@test.com")

    user_res = await client.get("/users/me", headers=headers)
    user_id = user_res.json()["id"]

    import asyncio
    from functools import partial
    db = next(get_db())
    for i in range(60):
        await asyncio.get_running_loop().run_in_executor(
            None, partial(create_log, db, user_id, f"action_{i}", "test")
        )

    res = await client.get("/audit-log/", headers=headers)
    assert res.status_code == 200
    logs = res.json()
    assert len(logs) <= 50  # ברירת מחדל של limit=50
    timestamps = [datetime.fromisoformat(log["timestamp"]) for log in logs]
    assert timestamps == sorted(timestamps, reverse=True)

@pytest.mark.asyncio
async def test_unauthorized_access():
    async with AsyncClient(app=app, base_url="http://test") as client:
        res = await client.get("/audit-log/")
        assert res.status_code == 401

@pytest.mark.asyncio
async def test_create_log_without_optional_fields(client):
    headers = await register_and_login(client, email="optional@test.com")

    user_res = await client.get("/users/me", headers=headers)
    user_id = user_res.json()["id"]

    import asyncio
    from functools import partial
    db = next(get_db())
    await asyncio.get_running_loop().run_in_executor(
        None, partial(create_log, db, user_id, "login", "user")
    )

    res = await client.get("/audit-log/", headers=headers)
    assert res.status_code == 200
    logs = res.json()
    assert any(log["action"] == "login" for log in logs)

@pytest.mark.asyncio
async def test_audit_log_response_schema(client):
    headers = await register_and_login(client, email="schema@test.com")

    user_res = await client.get("/users/me", headers=headers)
    user_id = user_res.json()["id"]

    import asyncio
    from functools import partial
    db = next(get_db())
    await asyncio.get_running_loop().run_in_executor(
        None, partial(create_log, db, user_id, "test", "schema", 1, "test details")
    )

    res = await client.get("/audit-log/", headers=headers)
    assert res.status_code == 200
    logs = res.json()
    for log in logs:
        assert "id" in log
        assert "user_id" not in log
        assert "action" in log
        assert "entity_type" in log
        assert "entity_id" in log
        assert "details" in log
        assert "timestamp" in log

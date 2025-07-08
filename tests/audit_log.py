import pytest

@pytest.mark.asyncio
async def test_audit_log_entry_on_client_create(client):
    await client.post("/users/register", json={
        "email": "audit@test.com",
        "password": "12345678",
        "full_name": "Audit Bot"
    })
    login = await client.post("/users/login", json={
        "email": "audit@test.com",
        "password": "12345678"
    })
    token = login.json()["access_token"]

    res = await client.post(
        "/clients/",
        json={"name": "Log Test", "address": "Anywhere"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert res.status_code == 200

    logs = await client.get("/audit-log/", headers={"Authorization": f"Bearer {token}"})
    assert logs.status_code == 200
    assert any("Created client" in log["details"] for log in logs.json())

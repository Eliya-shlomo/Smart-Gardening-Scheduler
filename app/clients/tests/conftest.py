import pytest
from httpx import AsyncClient

USERS_URL = "http://localhost:8001"   
CLIENTS_URL = "http://localhost:8002"  
EMAILLOGS_URL = "http://localhost:8002"  

@pytest.fixture
async def user_token():
    async with AsyncClient(base_url=USERS_URL) as client:
        email = "testuser_" + __import__('uuid').uuid4().hex[:6] + "@test.com"
        await client.post("/users/register", json={
            "email": email,
            "password": "12345678",
            "name": "Test User",
            "phone": "0501234567"
        })
        login = await client.post("/users/login", json={
            "email": email,
            "password": "12345678"
        })
        token = login.json()["access_token"]
        yield {"Authorization": f"Bearer {token}"}

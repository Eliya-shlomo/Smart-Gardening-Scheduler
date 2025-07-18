import httpx
from fastapi import Request

CLIENT_SERVICE_URL = "http://localhost:8002"

async def verify_client_access(client_id: int, request: Request):
    async with httpx.AsyncClient() as client:
        headers = {"Authorization": request.headers.get("Authorization")}
        response = await client.get(f"{CLIENT_SERVICE_URL}/clients/{client_id}/access", headers=headers)
        if response.status_code != 200:
            raise HTTPException(status_code=403, detail="No access to this client")
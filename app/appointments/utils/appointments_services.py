import httpx
from fastapi import Header, HTTPException, status

async def verify_client_ownership(client_id: int, user_id: int, token: str) -> bool:
    try:
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"http://localhost:8002/clients/{client_id}",
                headers=headers
            )
        if resp.status_code == 200 and resp.json()["user_id"] == user_id:
            return True
        return False
    except Exception:
        return False



def get_token(authorization: str = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header"
        )
    return authorization[7:]
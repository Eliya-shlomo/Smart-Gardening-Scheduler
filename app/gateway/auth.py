from fastapi import Request, HTTPException, status, Depends
from shared.jwt_utils import decode_access_token

def verify_jwt_token(request: Request):
    """
    Dependency for FastAPI.
    Checks Authorization header, validates JWT using decode_access_token from shared module.
    Returns claims if valid, otherwise raises HTTP 401.
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header"
        )
    token = auth_header.split(" ")[1]
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    return payload  

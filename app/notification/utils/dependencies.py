import os
import requests
from fastapi import Depends, HTTPException, status, Header
from typing import Optional


USERS_URL = "http://localhost:8001/users/me"  

def get_current_user(authorization: Optional[str] = Header(None)):
    try:
        headers = {"Authorization": authorization}
        resp = requests.get(USERS_URL, headers=headers, timeout=3)
        if resp.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid token or user service unavailable")
        return resp.json()
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"User authentication failed: {e}")

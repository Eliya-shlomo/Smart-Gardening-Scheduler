from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from users.schemas.token import Token
from users.crud.refresh_token import get_valid_refresh_token
from users.utils.security import create_access_token
from users.database import get_db

router = APIRouter()

@router.post("/refresh-token", response_model=Token)
def refresh_token(
    refresh_token: str = Body(...),
    db: Session = Depends(get_db)
):

    token_record = get_valid_refresh_token(db, refresh_token)
    if not token_record:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    access_token = create_access_token(data={"sub": str(token_record.user_id)})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.users.crud.refresh_token import get_valid_refresh_token, revoke_refresh_token
from app.users.api.deps import get_current_user
from app.users.database import get_db
from app.users.utils.audit_logger import send_audit_log
from app.users.models.user import User

router = APIRouter()

@router.post("/logout")
def logout(
    refresh_token: str = Body(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    token_record = get_valid_refresh_token(db, refresh_token)
    if not token_record or token_record.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized token")

    revoke_refresh_token(db, refresh_token)

    # Audit Log for login
    send_audit_log(
        user_id=user.id,
        action="login",
        entity_type="User",
        details=f"User {user.email} logged in"
    )

    return {"detail": "Logged out successfully"}

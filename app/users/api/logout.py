from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from users.crud.refresh_token import get_valid_refresh_token, revoke_refresh_token
from users.utils.deps import get_current_user
from users.database import get_db
from users.utils.audit_logger import send_log
from users.models.user import User

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

    # Audit Log for **logout**
    send_log(
        user_id=current_user.id,  
        action="logout",          
        entity_type="User",
        details=f"User {current_user.email} logged out"   
    )

    return {"detail": "Logged out successfully"}

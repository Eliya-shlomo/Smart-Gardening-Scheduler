from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.audit_log import AuditLogResponse
from app.audit.crud.audit_log import get_logs_for_user

router = APIRouter(prefix="/audit-log", tags=["Audit Trail"])

@router.get("/", response_model=list[AuditLogResponse])
def get_my_logs(
    user_id: int = Query(...), 
    db: Session = Depends(get_db)
):
    return get_logs_for_user(db, user_id)

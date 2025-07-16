from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from audit.database import get_db
from audit.schemas.audit import AuditLogCreate, AuditLogResponse
from audit.crud.audit import create_log, get_logs_for_user

router = APIRouter(tags=["Audit"])

@router.post("/", status_code=201, response_model=AuditLogResponse)
def create_log_endpoint(
    log: AuditLogCreate,
    db: Session = Depends(get_db)
):
    return create_log(
        db=db,
        user_id=log.user_id,
        action=log.action,
        entity_type=log.entity_type,
        entity_id=log.entity_id,
        details=log.details
    )

@router.get("/", response_model=list[AuditLogResponse])
def get_logs(
    user_id: int = Query(..., description="User ID for which to fetch logs"),
    db: Session = Depends(get_db)
):
    return get_logs_for_user(db, user_id)

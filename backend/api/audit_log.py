from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.api.deps import get_current_user
from backend import models, crud
from backend.schemas.audit_log import AuditLogResponse
from backend.crud.audit_log import get_logs_for_user

router = APIRouter(prefix="/audit-log", tags=["Audit Trail"])

@router.get("/", response_model=list[AuditLogResponse])
def get_my_logs(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return get_logs_for_user(db, current_user.id)

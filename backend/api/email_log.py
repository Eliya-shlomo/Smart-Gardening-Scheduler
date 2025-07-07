from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.api.deps import get_current_user
from backend.schemas.email_log import EmailLogResponse
from backend import models
from backend.services.reports import get_email_logs_summary

router = APIRouter(prefix="/emaillogs", tags=["Email Logs"])

@router.get("/", response_model=list[EmailLogResponse])
def get_email_logs(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return db.query(models.EmailLog).filter(models.EmailLog.recipient_email.in_(
        [c.email for c in current_user.clients]
    )).order_by(models.EmailLog.sent_at.desc()).all()



@router.get("/emails")
def email_logs_summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return get_email_logs_summary(db, current_user)
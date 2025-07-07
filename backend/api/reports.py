from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime
from backend.database import get_db
from backend.api.deps import get_current_user
from backend import models
from backend.services.reports import get_monthly_report_logic, get_email_logs_summary

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/monthly")
def get_monthly_report(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return get_monthly_report_logic(db, current_user)


@router.get("/emails")
def email_logs_summary(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return get_email_logs_summary(db, current_user)
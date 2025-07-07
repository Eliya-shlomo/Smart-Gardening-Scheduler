from datetime import datetime
from typing import Counter
from sqlalchemy.orm import Session
from backend import models

def get_monthly_report_logic(db: Session, user: models.User):
    now = datetime.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    clients = db.query(models.Client).filter(
        models.Client.user_id == user.id,
        models.Client.created_at >= start_of_month
    ).count() if hasattr(models.Client, "created_at") else None

    appointments = db.query(models.Appointment).join(models.Client).filter(
        models.Client.user_id == user.id,
        models.Appointment.date >= start_of_month
    ).all()

    total_appointments = len(appointments)
    completed_appointments = sum(1 for a in appointments if a.status == "done")

    recommendations = db.query(models.Recommendation).join(models.Tree).join(models.Client).filter(
        models.Client.user_id == user.id,
        models.Recommendation.send_date >= start_of_month
    ).count()

    return {
        "month": now.strftime("%B %Y"),
        "new_clients": clients,
        "appointments_total": total_appointments,
        "appointments_done": completed_appointments,
        "recommendations_sent": recommendations
    }



def get_email_logs_summary(db: Session, user: models.User):
    now = datetime.now()
    start_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    client_emails = [c.email for c in user.clients]

    logs = db.query(models.EmailLog).filter(
        models.EmailLog.recipient_email.in_(client_emails),
        models.EmailLog.sent_at >= start_of_month
    ).all()

    sent = sum(1 for log in logs if log.status == "sent")
    failed = sum(1 for log in logs if log.status == "failed")

    per_client = Counter(log.recipient_email for log in logs)

    return {
        "month": now.strftime("%B %Y"),
        "total_sent": sent,
        "total_failed": failed,
        "by_client": per_client
    }
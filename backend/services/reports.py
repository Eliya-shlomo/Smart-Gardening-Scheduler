from datetime import datetime
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

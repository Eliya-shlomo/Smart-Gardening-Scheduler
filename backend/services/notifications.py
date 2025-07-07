from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from backend.models import Appointment, EmailLog
from backend.services.mailer import send_email

def notify_clients_before_appointments(db: Session):
    now = datetime.now()
    reminder_window = timedelta(hours=1)

    appointments = db.query(Appointment).filter(
        Appointment.status == "scheduled",
        Appointment.date >= now,
        Appointment.date <= now + reminder_window
    ).all()

    for appt in appointments:
        client = appt.client
        user = client.user

        subject = "תזכורת לפגישה עם הגנן"
        body = (
            f"שלום {client.name},\n\n"
            f"זוהי תזכורת לפגישה הקרובה שלך עם הגנן {user.name}.\n"
            f"תאריך: {appt.date.strftime('%d/%m/%Y %H:%M')}\n"
            f"סוג טיפול: {appt.treatment_type}\n\n"
            f"בברכה,\nמערכת ניהול הגינון"
        )

        html_body = body.replace('\n', '<br>')
        html_message = f"<html><body dir='rtl'><p>{html_body}</p></body></html>"

        try:
            send_email(to_email=client.email, subject=subject, body=html_message, html=True)
            status = "sent"
        except Exception as e:
            status = f"failed: {str(e)}"

        db.add(EmailLog(
            template_name="appointment_reminder",
            recipient_email=client.email,
            status=status
        ))

    db.commit()


def notify_clients_after_appointments(db: Session):
    now = datetime.now()
    followup_window = timedelta(minutes=10)

    appointments = db.query(Appointment).filter(
        Appointment.status == "done",
        Appointment.date <= now,
        Appointment.date >= now - followup_window
    ).all()

    for appt in appointments:
        client = appt.client
        user = client.user

        subject = "תודה שהשתתפת בפגישה"
        body = (
            f"שלום {client.name},\n\n"
            f"תודה שהשתתפת בפגישה עם הגנן {user.name}.\n"
            f"נשמח לשמוע ממך פידבק או לעזור בפעם הבאה.\n\n"
            f"בברכה,\nמערכת ניהול הגינון"
        )

        html_body = body.replace('\n', '<br>')
        html_message = f"<html><body dir='rtl'><p>{html_body}</p></body></html>"

        try:
            send_email(to_email=client.email, subject=subject, body=html_message, html=True)
            status = "sent"
        except Exception as e:
            status = f"failed: {str(e)}"

        db.add(EmailLog(
            template_name="appointment_followup",
            recipient_email=client.email,
            status=status
        ))

    db.commit()

from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from backend.models import Appointment, EmailLog, Client, User
from backend.database import SessionLocal
from .mailer import send_email

def notify_clients_about_tomorrow_appointments():
    db: Session = SessionLocal()
    tomorrow = datetime.now().date() + timedelta(days=1)

    appointments = (
        db.query(Appointment)
        .filter(
            Appointment.date == tomorrow,
            Appointment.status == "scheduled"
        )
        .all()
    )

    for appt in appointments:
        client = appt.client
        subject = f"יש לך טיפול מחר ({appt.date.strftime('%d/%m/%Y')})"
        message = (
            f"שלום {client.name},\n\n"
            f"תזכורת לטיפול שתואם למחר:\n"
            f"- סוג טיפול: {appt.treatment_type}\n"
            f"- שעה: {appt.time}\n\n"
            f"בברכה,\nמערכת ניהול הגינון"
        )
        message_html = message.replace('\n', '<br>')

        html_message = f"""
        <html>
        <body dir="rtl" style="font-family: Arial, sans-serif; text-align: right;">
            <p>{message_html}</p>
        </body>
        </html>
        """

        try:
            send_email(
                to_email=client.email,
                subject=subject,
                body=html_message,
                html=True
            )
            status = "success"
        except Exception as e:
            status = f"failed: {e}"

        log = EmailLog(
            template_name="client_notification",
            recipient_email=client.email,
            status=status
        )
        db.add(log)

    db.commit()
    db.close()


def notify_gardeners_about_tomorrow_appointments():
    db: Session = SessionLocal()
    tomorrow = datetime.now().date() + timedelta(days=1)

    # שלוף את כל הפגישות למחר
    appointments = (
        db.query(Appointment)
        .filter(
            Appointment.date == tomorrow,
            Appointment.status == "scheduled"
        )
        .all()
    )

    # ארגן לפי גנן
    appointments_by_gardener = {}

    for appt in appointments:
        gardener = appt.client.user
        if gardener.id not in appointments_by_gardener:
            appointments_by_gardener[gardener.id] = {
                "gardener": gardener,
                "appointments": []
            }
        appointments_by_gardener[gardener.id]["appointments"].append(appt)

    for gardener_id, data in appointments_by_gardener.items():
        gardener = data["gardener"]
        appts = data["appointments"]

        subject = f"רשימת הטיפולים שלך למחר ({tomorrow.strftime('%d/%m/%Y')})"
        message_lines = []
        for appt in appts:
            client = appt.client
            line = (
                f"- לקוח: {client.name}\n"
                f"  סוג טיפול: {appt.treatment_type}\n"
                f"  שעה: {appt.time}\n"
            )
            message_lines.append(line)

        message_body = "\n".join(message_lines)
        full_message = (
            f"שלום {gardener.name},\n\n"
            f"הנה רשימת הטיפולים שלך למחר:\n\n"
            f"{message_body}\n"
            f"בברכה,\nמערכת ניהול הגינון"
        )

        message_html = full_message.replace('\n', '<br>')

        html_message = f"""
        <html>
        <body dir="rtl" style="font-family: Arial, sans-serif; text-align: right;">
            <p>{message_html}</p>
        </body>
        </html>
        """

        try:
            send_email(
                to_email=gardener.email,
                subject=subject,
                body=html_message,
                html=True
            )
            status = "success"
        except Exception as e:
            status = f"failed: {e}"

        log = EmailLog(
            template_name="gardener_summary",
            recipient_email=gardener.email,
            status=status
        )
        db.add(log)

    db.commit()
    db.close()





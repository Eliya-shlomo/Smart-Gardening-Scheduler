import html
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from backend.config import settings
from backend.crud import email_log  
from backend.database import SessionLocal



def send_email(to_email: str, subject: str, body: str, template_name: str = "default", html: bool = False):
    sender_email = settings.MAIL_FROM
    smtp_server = settings.SMTP_SERVER
    smtp_port = settings.SMTP_PORT
    smtp_username = settings.SMTP_USERNAME
    smtp_password = settings.SMTP_PASSWORD

    msg = MIMEMultipart("alternative")
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = subject

    if html:
        msg.attach(MIMEText(body, "html"))
    else:
        msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(smtp_username, smtp_password)
            server.send_message(msg)
        print(f"✅ Email sent to {to_email}")
        db = SessionLocal()
        email_log.create_log(db, template_name, to_email, "sent")
        db.close()

    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")
        db = SessionLocal()
        email_log.create_log(db, template_name, to_email, "failed")
        db.close()

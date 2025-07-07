from sqlalchemy.orm import Session
from backend import models

def create_log(db: Session, template_name: str, to_email: str, status: str):
    log = models.EmailLog(
        template_name=template_name,
        recipient_email=to_email,
        status=status
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

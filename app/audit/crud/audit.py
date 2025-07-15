from sqlalchemy.orm import Session
from audit.models.audit import AuditLog

def create_log(
    db: Session,
    user_id: int,
    action: str,
    entity_type: str,
    entity_id: int = None,
    details: str = None
):
    log = AuditLog(
        user_id=user_id,
        action=action,
        entity_type=entity_type,
        entity_id=entity_id,
        details=details
    )
    db.add(log)
    db.commit()
    db.refresh(log)
    return log

def get_logs_for_user(db: Session, user_id: int, limit: int = 50):
    return db.query(AuditLog)\
        .filter(AuditLog.user_id == user_id)\
        .order_by(AuditLog.timestamp.desc())\
        .limit(limit).all()

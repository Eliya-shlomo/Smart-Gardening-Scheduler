from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from users.models.refresh_token import RefreshToken
from users.config import settings

def create_refresh_token(db: Session, token_str: str, user_id: int):
    expires_at = datetime.now() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    token = RefreshToken(
        token=token_str,
        user_id=user_id,
        expires_at=expires_at,
        revoked=False
    )
    db.add(token)
    db.commit()
    db.refresh(token)
    return token

def get_valid_refresh_token(db: Session, token_str: str):
    token = db.query(RefreshToken).filter(
        RefreshToken.token == token_str,
        RefreshToken.revoked == False,
        RefreshToken.expires_at > datetime.now()
    ).first()
    return token

def revoke_refresh_token(db: Session, token_str: str):
    token = db.query(RefreshToken).filter(
        RefreshToken.token == token_str
    ).first()
    if token:
        token.revoked = True
        db.commit()
    return token
from sqlalchemy.orm import Session
from backend import models
from backend.schemas.client import ClientCreate

def create_client(db: Session, client_in: ClientCreate, user_id: int):
    client = models.Client(**client_in.model_dump(), user_id=user_id)
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

def get_clients_for_user(db: Session, user_id: int):
    return db.query(models.Client).filter(models.Client.user_id == user_id).all()

def get_client(db: Session, client_id: int, user_id: int):
    return db.query(models.Client).filter(models.Client.id == client_id, models.Client.user_id == user_id).first()

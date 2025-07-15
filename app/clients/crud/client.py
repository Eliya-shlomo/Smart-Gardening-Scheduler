from sqlalchemy.orm import Session
from clients.models.client import Client
from clients.schemas.client import ClientCreate

def create_client(db: Session, client_in: ClientCreate, user_id: int):
    client = Client(**client_in.model_dump(), user_id=user_id)
    db.add(client)
    db.commit()
    db.refresh(client)
    return client

def get_clients_for_user(db: Session, user_id: int):
    return db.query(Client).filter(Client.user_id == user_id).all()

def get_client(db: Session, client_id: int, user_id: int):
    return db.query(Client).filter(Client.id == client_id, Client.user_id == user_id).first()

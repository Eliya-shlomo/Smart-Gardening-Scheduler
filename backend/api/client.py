from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.client import ClientCreate, ClientResponse
from backend.api.deps import get_current_user
from backend.crud.client import create_client,get_clients_for_user, get_client
from backend import models

router = APIRouter(prefix="/clients", tags=["Clients"])

@router.post("/", response_model=ClientResponse)
def create_client_route(client_in: ClientCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return create_client(db, client_in, current_user.id)

@router.get("/", response_model=list[ClientResponse])
def get_my_clients(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return get_clients_for_user(db, current_user.id)

@router.get("/{client_id}", response_model=ClientResponse)
def get_client_by_id(client_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    client = get_client(db, client_id, current_user.id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

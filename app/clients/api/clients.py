from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from clients.database import get_db
from clients.schemas.client import ClientCreate, ClientResponse
from clients.crud.client import create_client,get_clients_for_user, get_client
from clients.models.client import Client
from clients.utils.audit_logger import send_log
from clients.utils.dependencies import get_current_user




router = APIRouter(prefix="/clients", tags=["Clients"])

@router.post("/", response_model=ClientResponse)
def create_client_route(
    client_in: ClientCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    client = create_client(db, client_in, current_user["id"])
    send_log(
        user_id=current_user["id"],
        action="create",
        entity_type="Client",
        entity_id=client.id,
        details=f"Created client: {client.name}, address: {client.address}"
    )
    return client

    

@router.get("/", response_model=list[ClientResponse])
def get_my_clients(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return get_clients_for_user(db, current_user.id)

@router.get("/{client_id}", response_model=ClientResponse)
def get_client_by_id(client_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    client = get_client(db, client_id, current_user.id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.put("/{client_id}", response_model=ClientResponse)
def update_client(
    client_id: int,
    client_in: ClientCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    client = get_client(db, client_id, current_user.id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    client.name = client_in.name
    client.address = client_in.address
    client.phone = client_in.phone 

    db.commit()
    db.refresh(client)

    send_log(
        db=db,
        user_id=current_user.id,
        action="update",
        entity_type="Client",
        entity_id=client.id,
        details=f"Updated client: {client.name}"
    )

    return client



@router.delete("/{client_id}")
def delete_client(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    client = get_client(db, client_id, current_user.id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    db.delete(client)
    db.commit()

    send_log(
        db=db,
        user_id=current_user.id,
        action="delete",
        entity_type="Client",
        entity_id=client_id,
        details=f"Deleted client {client.name}"
    )

    return {"detail": "Client deleted"}

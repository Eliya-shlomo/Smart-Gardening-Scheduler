from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentResponse
from backend.api.deps import get_current_user
from backend import models
from backend.crud.appointment import create_appointment, get_appointments_for_client, get_appointment_by_id, update_appointment_status

router = APIRouter(prefix="/appointments", tags=["Appointments"])

@router.post("/", response_model=AppointmentResponse)
def create_appointment_view(
    appointment_in: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    client = db.query(models.Client).filter(
        models.Client.id == appointment_in.client_id,
        models.Client.user_id == current_user.id
    ).first()
    if not client:
        raise HTTPException(status_code=403, detail="Access denied to this client")

    return create_appointment(db, appointment_in)

@router.get("/client/{client_id}", response_model=list[AppointmentResponse])
def get_appointments_for_client_view(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    client = db.query(models.Client).filter(
        models.Client.id == client_id,
        models.Client.user_id == current_user.id
    ).first()
    if not client:
        raise HTTPException(status_code=403, detail="Access denied to this client")

    return get_appointments_for_client(db, client_id)

@router.patch("/{appointment_id}", response_model=AppointmentResponse)
def mark_appointment_done_view(
    appointment_id: int,
    update_data: AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    appointment = get_appointment_by_id(db, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if appointment.client.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied to this appointment")

    return update_appointment_status(db, appointment_id, update_data)

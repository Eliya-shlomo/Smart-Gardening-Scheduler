from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from scheduler.database import get_db
from scheduler.schemas.appointment import AppointmentCreate, AppointmentUpdate, AppointmentResponse
from scheduler.utils.deps import get_current_user
from backend.models import User, Appointment, Client
from backend.crud.appointment import (
    create_appointment,
    get_appointments_for_client,
    get_appointment_by_id,
    update_appointment_status
)
from backend.crud.audit_log import create_log

router = APIRouter(prefix="/appointments", tags=["Appointments"])


@router.post("/", response_model=AppointmentResponse)
def create_appointment_view(
    appointment_in: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    client = db.query(Client).filter(
        Client.id == appointment_in.client_id,
        Client.user_id == current_user.id
    ).first()
    if not client:
        raise HTTPException(status_code=403, detail="Access denied to this client")

    appointment = create_appointment(db, appointment_in)

    create_log(
        db=db,
        user_id=current_user.id,
        action="create",
        entity_type="Appointment",
        entity_id=appointment.id,
        details=f"Created appointment for client_id={appointment_in.client_id} on {appointment_in.date}"
    )

    return appointment


@router.get("/client/{client_id}", response_model=list[AppointmentResponse])
def get_appointments_for_client_view(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    client = db.query(Client).filter(
        Client.id == client_id,
        Client.user_id == current_user.id
    ).first()
    if not client:
        raise HTTPException(status_code=403, detail="Access denied to this client")

    return get_appointments_for_client(db, client_id)


@router.patch("/{appointment_id}", response_model=AppointmentResponse)
def mark_appointment_done_view(
    appointment_id: int,
    update_data: AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    appointment = get_appointment_by_id(db, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    if appointment.client.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied to this appointment")

    updated = update_appointment_status(db, appointment_id, update_data)

    create_log(
        db=db,
        user_id=current_user.id,
        action="update",
        entity_type="Appointment",
        entity_id=appointment.id,
        details=f"Updated status of appointment {appointment.id} to {updated.status}"
    )

    return updated


@router.put("/{appointment_id}", response_model=AppointmentResponse)
def update_appointment(
    appointment_id: int,
    appointment_in: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment or appointment.client.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    appointment.date = appointment_in.date
    appointment.status = appointment_in.status
    appointment.notes = appointment_in.notes
    db.commit()
    db.refresh(appointment)

    create_log(
        db=db,
        user_id=current_user.id,
        action="update",
        entity_type="Appointment",
        entity_id=appointment.id,
        details=f"Updated appointment {appointment.id} to status={appointment.status}"
    )

    return appointment


@router.delete("/{appointment_id}")
def delete_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment or appointment.client.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    log_details = f"Deleted appointment on {appointment.date} for client_id={appointment.client_id}"

    db.delete(appointment)

    create_log(
        db=db,
        user_id=current_user.id,
        action="delete",
        entity_type="Appointment",
        entity_id=appointment_id,
        details=log_details
    )

    db.commit()

    return {"detail": "Appointment deleted"}

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from appointments.database import get_db
from appointments.utils.get_current_user import get_current_user
from appointments.models.appointments import AppointmentStatus, Appointment
from appointments.schemas.appointments import AppointmentCreate, AppointmentUpdate, AppointmentResponse
from appointments.crud.appointments import update_appointment_status, get_appointment_by_id,get_appointments_for_client ,create_appointment
from appointments.utils.audit_logger import send_log
from appointments.utils.appoinments_services import verify_client_ownership, get_token



router = APIRouter(tags=["Appointments"])


@router.post("/", response_model=AppointmentResponse)
async def create_appointment_view(
    appointment_in: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    token: str = Depends(get_token)  
):
    if not await verify_client_ownership(appointment_in.client_id, current_user["id"], token):
        raise HTTPException(status_code=403, detail="Access denied to this client")

    appointment = create_appointment(db, appointment_in)

    send_log(
        user_id=current_user["id"], 
        action="create",
        entity_type="Appointment",
        entity_id=appointment.id,
        details=f"Created appointment for client_id={appointment_in.client_id} on {appointment_in.date}"
    )

    return appointment


@router.get("/client/{client_id}", response_model=list[AppointmentResponse])
async def get_appointments_for_client_view(
    client_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    request: Request = None,
    token: str = Depends(get_token)  

):
    # token = request.headers.get("Authorization", "")
    if not await verify_client_ownership(client_id, current_user["id"], token):
        raise HTTPException(status_code=403, detail="Access denied to this client")

    return get_appointments_for_client(db, client_id)



@router.patch("/{appointment_id}", response_model=AppointmentResponse)
async def mark_appointment_done_view(
    appointment_id: int,
    update_data: AppointmentUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    request: Request = None,
    token: str = Depends(get_token)  
):
    appointment = get_appointment_by_id(db, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    # token = request.headers.get("Authorization", "")
    if not await verify_client_ownership(appointment.client_id, current_user["id"], token):
        raise HTTPException(status_code=403, detail="Access denied to this appointment")

    updated = update_appointment_status(db, appointment_id, update_data)

    send_log(
        user_id=current_user["id"],
        action="update",
        entity_type="Appointment",
        entity_id=appointment.id,
        details=f"Updated status of appointment {appointment.id} to {updated.status}"
    )

    return updated


@router.put("/{appointment_id}", response_model=AppointmentResponse)
async def update_appointment_view(
    appointment_id: int,
    appointment_in: AppointmentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    request: Request = None,
    token: str = Depends(get_token)  
):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    # token = request.headers.get("Authorization", "")
    if not await verify_client_ownership(appointment.client_id, current_user["id"], token):
        raise HTTPException(status_code=403, detail="Unauthorized")

    appointment.date = appointment_in.date
    appointment.time = appointment_in.time
    appointment.status = appointment_in.status
    appointment.notes = appointment_in.notes
    appointment.treatment_type = appointment_in.treatment_type
    
    db.commit()
    db.refresh(appointment)

    send_log(
        user_id=current_user["id"],
        action="update",
        entity_type="Appointment",
        entity_id=appointment.id,
        details=f"Updated appointment {appointment.id} to status={appointment.status}"
    )

    return appointment



@router.delete("/{appointment_id}")
async def delete_appointment_view(
    appointment_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    request: Request = None,
    token: str = Depends(get_token)  

):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    # token = request.headers.get("Authorization", "")
    if not await verify_client_ownership(appointment.client_id, current_user["id"], token):
        raise HTTPException(status_code=403, detail="Unauthorized")

    log_details = f"Deleted appointment on {appointment.date} for client_id={appointment.client_id}"

    db.delete(appointment)

    send_log(
        user_id=current_user["id"],
        action="delete",
        entity_type="Appointment",
        entity_id=appointment_id,
        details=log_details
    )

    db.commit()

    return {"detail": "Appointment deleted"}

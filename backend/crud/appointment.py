from sqlalchemy.orm import Session
from backend import models
from backend.schemas.appointment import AppointmentCreate, AppointmentUpdate

def create_appointment(db: Session, appointment_in: AppointmentCreate):
    appointment = models.Appointment(**appointment_in.model_dump())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment

def get_appointments_for_client(db: Session, client_id: int):
    return db.query(models.Appointment).filter(models.Appointment.client_id == client_id).all()

def get_appointment_by_id(db: Session, appointment_id: int):
    return db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()

def update_appointment_status(db: Session, appointment_id: int, update_data: AppointmentUpdate):
    appointment = get_appointment_by_id(db, appointment_id)
    if appointment:
        appointment.status = update_data.status
        appointment.notes = update_data.notes or appointment.notes
        db.commit()
        db.refresh(appointment)
    return appointment

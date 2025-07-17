from sqlalchemy import Column, Integer, String, DateTime, Text, Enum
from appointments.database import Base
import enum

class AppointmentStatus(str, enum.Enum): 
    pending = "pending"
    done = "done"

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    time = Column(String, nullable=False)
    treatment_type = Column(String, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.pending, nullable=False)
    notes = Column(Text)
    client_id = Column(Integer, nullable=False)

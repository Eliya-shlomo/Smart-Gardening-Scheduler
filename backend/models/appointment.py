from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship, declarative_base
import enum
from backend.database import Base


class AppointmentStatus(enum.Enum):
    scheduled = "scheduled"
    done = "done"


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False)
    time = Column(String, nullable=False)  
    treatment_type = Column(String, nullable=False)
    status = Column(Enum(AppointmentStatus), default=AppointmentStatus.scheduled)
    notes = Column(Text)
    client_id = Column(Integer, ForeignKey("clients.id"))

    client = relationship("Client", back_populates="appointments")
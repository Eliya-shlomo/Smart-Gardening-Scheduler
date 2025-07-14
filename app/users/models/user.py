from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship, declarative_base
from backend.database import Base
## the base schema on db. by using the user it possible to do the rest of action on db(after verifying its truly the user by func get_current_user  )

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    phone = Column(String)

    clients = relationship("Client", back_populates="user")
    audit_logs = relationship("AuditLog", back_populates="user")

from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship, declarative_base
from clients.database import Base
from sqlalchemy.sql import func

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    address = Column(String)
    phone = Column(String)
    user_id = Column(Integer, nullable=False)  
    created_at = Column(DateTime, server_default=func.now())


 
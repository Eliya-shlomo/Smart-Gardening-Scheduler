from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class EmailLog(Base):
    __tablename__ = "email_logs"

    id = Column(Integer, primary_key=True, index=True)
    template_name = Column(String, nullable=False)
    sent_at = Column(DateTime, default=datetime.utcnow)
    recipient_email = Column(String, nullable=False)
    status = Column(String)  

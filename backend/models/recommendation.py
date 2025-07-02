from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime
from backend.database import Base

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)  
    send_date = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)
    tree_id = Column(Integer, ForeignKey("trees.id"))

    tree = relationship("Tree", back_populates="recommendations")
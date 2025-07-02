from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship, declarative_base
from backend.database import Base

class Tree(Base):
    __tablename__ = "trees"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    planting_date = Column(DateTime)
    notes = Column(Text)
    client_id = Column(Integer, ForeignKey("clients.id"))

    client = relationship("Client", back_populates="trees")
    recommendations = relationship("Recommendation", back_populates="tree")

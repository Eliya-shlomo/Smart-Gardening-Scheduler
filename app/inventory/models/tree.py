from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship, declarative_base
from inventory.database import Base

class Tree(Base):
    __tablename__ = "trees"

    id = Column(Integer, primary_key=True, index=True)
    type = Column(String, nullable=False)
    planting_date = Column(DateTime)
    notes = Column(Text)
    client_id = Column(Integer, nullable=False) 


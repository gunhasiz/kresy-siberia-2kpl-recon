from typing import Any

from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import _RelationshipDeclared
from .base import Base

class DeportationAndRepression(Base):
    __tablename__: str = "deportations_and_repressions"

    id: Column[int] = Column(Integer, primary_key=True)
    person_id: Column[int] = Column(Integer, ForeignKey("people.id"), nullable=False)
    
    description: Column[str] = Column(Text)
    other_information: Column[str] = Column(Text)

    person: _RelationshipDeclared[Any] = relationship("Person", back_populates="deportations_and_repressions")
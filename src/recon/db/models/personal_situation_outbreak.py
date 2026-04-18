from typing import Any

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import _RelationshipDeclared
from .base import Base

class PersonalSituationOutbreakOfWWII(Base):
    __tablename__: str = "personal_situation_outbreaks_of_wwii"

    id: Column[int] = Column(Integer, primary_key=True)
    person_id: Column[int] = Column(Integer, ForeignKey("persons.id"), nullable=False)
    
    # Residence at the outbreak of WWII
    residence: Column[str] = Column(String, nullable=True)
    # Kresy Inhabitant Status:
    kresy_inhabitant_status: Column[str] = Column(String, nullable=True)
    # Ethnicity
    ethnicity: Column[str] = Column(String, nullable=True)
    # Religion
    religion: Column[str] = Column(String, nullable=True)
    # Education Level
    education_level: Column[str] = Column(String, nullable=True)
    # Occupation at the outbreak of WWII
    occupation: Column[str] = Column(String, nullable=True)
    # Military status at the outbreak of WWII
    military_status: Column[str] = Column(String, nullable=True)
    # Military Rank at the outbreak of WWII
    military_rank: Column[str] = Column(String, nullable=True)

    person: _RelationshipDeclared[Any] = relationship("Person", back_populates="initial_status")
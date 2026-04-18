from typing import Any

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import _RelationshipDeclared
from .base import Base


class OtherMilitaryExperience(Base):
    __tablename__: str = "other_military_experiences"
    
    id: Column[int] = Column(Integer, primary_key=True)
    person_id: Column[int] = Column(
        Integer, ForeignKey("persons.id"), nullable=False)

    # General note about other wartime circumstances or military experience.
    information: Column[str] = Column(String, nullable=True)
    # Name or description of orphanage placement (institution name, role, or context).
    orphanages: Column[str] = Column(String, nullable=True)
    # Details of civilian camp in the Middle East (name, location, purpose, dates if known).
    civilian_camp_middle_east: Column[str] = Column(String, nullable=True)
    # Details of civilian camp in India (name, location, purpose, dates if known).
    civilian_camp_india: Column[str] = Column(String, nullable=True)
    # Details of civilian camp in Africa (name, location, purpose, dates if known).
    civilian_camp_africa: Column[str] = Column(String, nullable=True)
    # Any additional free‑text information not covered by the other fields.
    other_information: Column[str] = Column(String, nullable=True)

    person: _RelationshipDeclared[Any] = relationship(
        "Person", back_populates="other_military_experiences")
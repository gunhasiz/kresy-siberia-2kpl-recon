from datetime import date
from typing import Any

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import _RelationshipDeclared

from .base import BaseDTO


class MilitaryExperienceDTO(BaseDTO):
    __tablename__: str = "military_experiences"

    id: Column[int] = Column(Integer, primary_key=True)
    person_id: Column[int] = Column(
        Integer, ForeignKey("persons.id"), nullable=False)

    # Additional information about military service during WWII
    other_military_service: Column[str] = Column(String, nullable=True)
    # Participation in specific battles or campaigns during WWII
    participation_in_wwii_battles: Column[str] = Column(String, nullable=True)
    # Medals or honors received for miliatary service during WWII
    medals_received: Column[str] = Column(String, nullable=True)
    # Other information about participation in WWII battles or campaigns (If applicable)
    other_battles: Column[str] = Column(String, nullable=True)

    military_services: _RelationshipDeclared[Any] = relationship(
        "MilitaryServiceDTO", back_populates="military_experience")
    person: _RelationshipDeclared[Any] = relationship(
        "PersonDTO", back_populates="military_experiences")


class MilitaryServiceDTO(BaseDTO):
    __tablename__: str = "military_services"

    id: Column[int] = Column(Integer, primary_key=True)
    military_experience_id: Column[int] = Column(
        Integer, ForeignKey("military_experiences.id"), nullable=False)

    # Service branch (e.g., Army, Navy, Air Force, Other)
    service_branch: Column[str] = Column(String, nullable=True)
    # Military unit name or designation
    unit_name: Column[str] = Column(String, nullable=True)
    # Rank or position held during military service
    rank: Column[str] = Column(String, nullable=True)
    # Start date of military service (if known)
    from_when_date: Column[date] = Column(Date, nullable=True)
    # End date of military service (if known)
    to_when_date: Column[date] = Column(Date, nullable=True)

from datetime import date
from typing import Any

from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import _RelationshipDeclared
from .base import Base


class MilitaryExperience(Base):
    __tablename__: str = "military_experiences"

    id: Column[int] = Column(Integer, primary_key=True)
    person_id: Column[int] = Column(
        Integer, ForeignKey("persons.id"), nullable=False)

    military_services: _RelationshipDeclared[Any] = relationship(
        "MilitaryService", back_populates="military_experience")
    person: _RelationshipDeclared[Any] = relationship(
        "Person", back_populates="military_experiences")


class MilitaryService(Base):
    __tablename__: str = "military_services"

    id: Column[int] = Column(Integer, primary_key=True)
    military_experience_id: Column[int] = Column(
        Integer, ForeignKey("military_experiences.id"), nullable=False)

    # Service branch (e.g., Army, Navy, Air Force, Other)
    service_branch = Column(String, nullable=True)
    # Military unit name or designation
    unit_name = Column(String, nullable=True)
    # Rank or position held during military service
    rank = Column(String, nullable=True)
    # Start date of military service (if known)
    from_when_date = Column(Date, nullable=True)
    # End date of military service (if known)
    to_when_date = Column(Date, nullable=True)

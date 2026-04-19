from typing import Any
from datetime import date

from sqlalchemy import Boolean, Column, Date, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import _RelationshipDeclared

from .base import BaseDTO

class PersonDTO(BaseDTO):
    __tablename__ = "persons"
    
    id: Column[int] = Column(Integer, primary_key=True)
    
    # Entry ID
    external_entry_id: Column[int] = Column(Integer, unique=True, index=True)
    # Name
    full_name: Column[str] = Column(String, index=True)
    # Maiden Name
    maiden_name: Column[str] = Column(String, nullable=True)
    # Nickname/Pseudonym
    nickname: Column[str] = Column(String, nullable=True)
    # Gender
    gender: Column[str] = Column(String, nullable=True)
    # Date of birth
    birth_date: Column[date] = Column(Date, nullable=True)
    # Place of birth
    birth_place: Column[str] = Column(String, nullable=True)
    # Did this person die during World War ll?
    died_in_ww2: Column[bool] = Column(Boolean, default=False)
    # Date of death
    death_date: Column[date] = Column(Date, nullable=True)
    # Place of death
    death_place: Column[str] = Column(String, nullable=True)
    # Cause of death
    death_cause: Column[str] = Column(String, nullable=True)
    # Fathers given name
    father_name: Column[str] = Column(String, nullable=True)
    # Mothers given name
    mother_name: Column[str] = Column(String, nullable=True)
    # Mothers maiden name
    mother_maiden_name: Column[str] = Column(String, nullable=True)
    # Given name of spuse:
    spouse_name: Column[str] = Column(String, nullable=True)
    # Maiden name of spouse:
    spouse_maiden_name: Column[str] = Column(String, nullable=True)
    # Given name(s) of childern:
    children_names: Column[str] = Column(String, nullable=True)
    # Description
    description: Column[str] = Column(String, nullable=True)

    # TODO
    personal_situation_outbreak: _RelationshipDeclared[Any] = relationship("PersonalSituationOutbreak1939", back_populates="person", uselist=False)
    deportations_and_repressions: _RelationshipDeclared[Any] = relationship("DeportationAndRepression", back_populates="person")
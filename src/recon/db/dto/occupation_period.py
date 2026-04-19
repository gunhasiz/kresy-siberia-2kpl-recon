from typing import Any

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import _RelationshipDeclared

from .base import BaseDTO

class OccupationPeriodDTO(BaseDTO):
    __tablename__: str = "occupation_periods"

    id: Column[int] = Column(Integer, primary_key=True)
    person_id: Column[int] = Column(Integer, ForeignKey("persons.id"), nullable=False)

    # Place of province residence during occupation period
    province: Column[str] = Column(String, nullable=True)
    # Place of district residence during occupation period
    county: Column[str] = Column(String, nullable=True)
    # Place of city residence during occupation period
    city_place: Column[str] = Column(String, nullable=True)
    # Nearest large city to place of residence during occupation period
    nearest_large_city: Column[str] = Column(String, nullable=True)

    person: _RelationshipDeclared[Any] = relationship("PersonDTO", back_populates="occupation_periods")

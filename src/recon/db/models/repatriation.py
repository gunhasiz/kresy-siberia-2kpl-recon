from datetime import date
from typing import Any

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import _RelationshipDeclared
from .base import Base

class Repatriation(Base):
    __tablename__: str = "repatriations"

    id: Column[int] = Column(Integer, primary_key=True)
    person_id: Column[int] = Column(Integer, ForeignKey("persons.id"), nullable=False)

    # Date of return to Poland
    return_date: Column[date] = Column(Date, nullable=True)
    # Place of return to Poland
    province: Column[str] = Column(String, nullable=True)
    # District of return to Poland
    county: Column[str] = Column(String, nullable=True)
    # Locality of return to Poland
    locality: Column[str] = Column(String, nullable=True)
    # Nearest large city to place of return to Poland
    nearest_large_city: Column[str] = Column(String, nullable=True)

    person: _RelationshipDeclared[Any] = relationship("Person", back_populates="repatriations")
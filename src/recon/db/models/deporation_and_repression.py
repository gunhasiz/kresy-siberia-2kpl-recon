from datetime import date
from typing import Any

from sqlalchemy import Column, Integer, String, Date, Text, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import _RelationshipDeclared
from .base import Base

class DeportationAndRepression(Base):
    __tablename__: str = "deportations_and_repressions"

    id: Column[int] = Column(Integer, primary_key=True)
    person_id: Column[int] = Column(Integer, ForeignKey("persons.id"), nullable=False)
    place_id: Column[int] = Column(Integer, ForeignKey("places.id"), nullable=True)

    # Other information about deportation or repression
    other_information: Column[str] = Column(Text)

    place: _RelationshipDeclared[Any] = relationship("Places")
    person: _RelationshipDeclared[Any] = relationship("Person", back_populates="deportations_and_repressions")

class Places(Base):
    __tablename__: str = "places"

    id: Column[int] = Column(Integer, primary_key=True)

    # When deportation or repression took place
    from_when_date: Column[date] = Column(Date, nullable=True)
    # When deportation or repression ended (if applicable)
    to_when_date: Column[date] = Column(Date, nullable=True)
    # Authority or institution that ordered or carried out the deportation or repression
    deporting_authority: Column[str] = Column(String, nullable=True)
    # Location of deportation or repression
    oblast: Column[str] = Column(String, nullable=True)
    # City or town of deportation or repression
    city: Column[str] = Column(String, nullable=True)
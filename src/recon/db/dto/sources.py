from typing import Any

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import _RelationshipDeclared

from .base import BaseDTO

class SourcesDTO(BaseDTO):
    __tablename__: str = "sources"
    
    id: Column[int] = Column(Integer, primary_key=True)
    person_id: Column[int] = Column(
        Integer, ForeignKey("persons.id"), nullable=False)

    # A brief summary or description of the source
    summary: Column[str] = Column(String, nullable=True)
    # URL or reference to the source in string form
    url_text: Column[str] = Column(String, nullable=True)
    # URL or reference to the source
    url: Column[str] = Column(String, nullable=True)

    person: _RelationshipDeclared[Any] = relationship(
        "PersonDTO", back_populates="sources")
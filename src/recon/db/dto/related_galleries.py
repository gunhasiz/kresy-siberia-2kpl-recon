from typing import Any

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import _RelationshipDeclared

from .base import BaseDTO

class RelatedGalleriesDTO(BaseDTO):
    __tablename__: str = "related_galleries"
    
    id: Column[int] = Column(Integer, primary_key=True)
    person_id: Column[int] = Column(
        Integer, ForeignKey("persons.id"), nullable=False)

    # A brief summary or description of the source
    summary = Column(String, nullable=True)
    # URL or reference to the source in string form
    url_text = Column(String, nullable=True)
    # URL or reference to the source
    url = Column(String, nullable=True)

    person: _RelationshipDeclared[Any] = relationship(
        "PersonDTO", back_populates="related_galleries")
from typing import Any

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.relationships import _RelationshipDeclared

from .base import BaseDTO

class StatusDTO(BaseDTO):
    __tablename__: str = "statuses"
    
    id: Column[int] = Column(Integer, primary_key=True)

    # Id of an entry in the main table
    entry_id: Column[str] = Column(String, nullable=True)
    # URL or reference to the source
    url: Column[str] = Column(String, nullable=True)
    # Scrape status (e.g., "pending", "in_progress", "completed", "failed")
    status: Column[str] = Column(String, nullable=True)
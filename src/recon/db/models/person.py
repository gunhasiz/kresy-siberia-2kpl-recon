from sqlalchemy import Column, Integer, String, DateTime, func

from .base import Base

class Person(Base):
    __tablename__ = "persons"
    
    id = Column(Integer, primary_key=True)
    external_id = Column(String, unique=True, index=True)
    first_name = Column(String)
    last_name = Column(String, index=True)
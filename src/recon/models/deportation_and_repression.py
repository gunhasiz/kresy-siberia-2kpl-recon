from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class Place(BaseModel):
    from_when_date: Optional[date] = None
    to_when_date: Optional[date] = None
    deporting_authority: Optional[str] = None
    oblast: Optional[str] = None
    city: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class DeportationAndRepression(BaseModel):
    other_information: Optional[str] = None
    place: Optional[Place] = None

    model_config = ConfigDict(from_attributes=True)
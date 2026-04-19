from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date

class MilitaryService(BaseModel):
    service_branch: Optional[str] = None
    unit_name: Optional[str] = None
    rank: Optional[str] = None
    from_when_date: Optional[date] = None
    to_when_date: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)

class MilitaryExperience(BaseModel):
    other_military_service: Optional[str] = None
    participation_in_wwii_battles: Optional[str] = None
    medals_received: Optional[str] = None
    other_battles: Optional[str] = None
    military_services: List[MilitaryService] = []

    model_config = ConfigDict(from_attributes=True)
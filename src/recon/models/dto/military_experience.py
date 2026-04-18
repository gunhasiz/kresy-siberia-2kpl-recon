from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date

class MilitaryServiceDTO(BaseModel):
    service_branch: Optional[str] = None
    unit_name: Optional[str] = None
    rank: Optional[str] = None
    from_when_date: Optional[date] = None
    to_when_date: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)

class MilitaryExperienceDTO(BaseModel):
    other_military_service: Optional[str] = None
    participation_in_wwii_battles: Optional[str] = None
    medals_received: Optional[str] = None
    other_battles: Optional[str] = None
    military_services: List[MilitaryServiceDTO] = []

    model_config = ConfigDict(from_attributes=True)
from pydantic import BaseModel, ConfigDict
from typing import Optional

class OtherMilitaryExperience(BaseModel):
    information: Optional[str] = None
    orphanages: Optional[str] = None
    civilian_camp_middle_east: Optional[str] = None
    civilian_camp_india: Optional[str] = None
    civilian_camp_africa: Optional[str] = None
    other_information: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
from pydantic import BaseModel, ConfigDict
from typing import Optional

class PersonalSituationOutbreakDTO(BaseModel):
    residence: Optional[str] = None
    kresy_inhabitant_status: Optional[str] = None
    ethnicity: Optional[str] = None
    religion: Optional[str] = None
    education_level: Optional[str] = None
    occupation: Optional[str] = None
    military_status: Optional[str] = None
    military_rank: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
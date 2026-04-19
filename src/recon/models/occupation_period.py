from pydantic import BaseModel, ConfigDict
from typing import Optional

class OccupationPeriod(BaseModel):
    province: Optional[str] = None
    county: Optional[str] = None
    city_place: Optional[str] = None
    nearest_large_city: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
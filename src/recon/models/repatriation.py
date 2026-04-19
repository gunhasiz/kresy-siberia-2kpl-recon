from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class Repatriation(BaseModel):
    return_date: Optional[date] = None
    province: Optional[str] = None
    county: Optional[str] = None
    locality: Optional[str] = None
    nearest_large_city: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
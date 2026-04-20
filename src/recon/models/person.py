from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class Person(BaseModel):
    external_entry_id: int
    full_name: Optional[str] = None
    maiden_name: Optional[str] = None
    nickname: Optional[str] = None
    gender: Optional[str] = None
    birth_date: Optional[date] = None
    birth_place: Optional[str] = None
    died_in_ww2: bool = False
    death_date: Optional[date] = None
    death_place: Optional[str] = None
    death_cause: Optional[str] = None
    father_name: Optional[str] = None
    mother_name: Optional[str] = None
    mother_maiden_name: Optional[str] = None
    spouse_name: Optional[str] = None
    spouse_maiden_name: Optional[str] = None
    children_names: Optional[str] = None
    description: Optional[str] = None

    model_config: ConfigDict = ConfigDict(from_attributes=True)
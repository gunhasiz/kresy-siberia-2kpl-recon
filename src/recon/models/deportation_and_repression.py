from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import date

class Place(BaseModel):
    from_when_date: Optional[date] = None
    to_when_date: Optional[date] = None
    from_yyyy: Optional[str] = None
    mm_first: Optional[str] = None
    dd_first: Optional[str] = None
    to_yyyy: Optional[str] = None
    mm_last: Optional[str] = None
    dd_last: Optional[str] = None
    deporting_authority: Optional[str] = None
    oblast: Optional[str] = None
    city: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
    
    # def model_post_init(self, __context):
    #     if self.from_yyyy and self.mm_first and self.dd_first:
    #         self.from_when_date = date(self.from_yyyy, self.mm_first, self.dd_first)

    #     if self.to_yyyy and self.mm_last and self.dd_last:
    #         self.to_when_date = date(self.to_yyyy, self.mm_last, self.dd_last)

class DeportationAndRepression(BaseModel):
    other_information: Optional[str] = None
    place: List[Place] = []

    model_config = ConfigDict(from_attributes=True)
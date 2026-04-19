from pydantic import BaseModel, ConfigDict
from typing import Optional

class Status(BaseModel):
    entry_id: Optional[str] = None
    url: Optional[str] = None
    status: Optional[str] = "pending"

    model_config = ConfigDict(from_attributes=True)
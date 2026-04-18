from pydantic import BaseModel, ConfigDict
from typing import Optional

class SourceDTO(BaseModel):
    summary: Optional[str] = None
    url_text: Optional[str] = None
    url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
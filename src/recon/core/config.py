from os import getenv
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Config:
    DATABASE_URL: Optional[str] = getenv("DATABASE_URL")
    DEBUG: bool = getenv("DEBUG", "False").lower() == "true"
    
    BASE_URL: Optional[str] = getenv("BASE_URL")
    USER_AGENT: Optional[str] = getenv("USER_AGENT")
    DELAY_MIN: float = float(getenv("DELAY_MIN", 1.0))
    DELAY_MAX: float = float(getenv("DELAY_MAX", 3.0))
    
    API_URL: Optional[str] = getenv("API_URL")
    CONCURRENT_REQUESTS: int = int(getenv("CONCURRENT_REQUESTS", 5))

config = Config()
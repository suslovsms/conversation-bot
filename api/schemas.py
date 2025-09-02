from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class UserCreate(BaseModel):
    telegram_id: str
    chat_id: str
    username: Optional[str]
    first_name: Optional[str]
    last_name: Optional[str]

class LogCreate(BaseModel):
    timestamp: Optional[datetime] = None
    level: str
    source: str
    message: str
    user_id: Optional[str] = None
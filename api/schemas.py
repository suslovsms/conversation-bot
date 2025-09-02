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

class MessageCreate(BaseModel):
    user_id: int
    user_message: str
    bot_response: str

class MessageResponse(MessageCreate):
    id: int
    timestamp: datetime

    class Config:
        orm_mode = True


class UserOut(UserCreate):
    id: int

    class Config:
        orm_mode = True
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database.database import get_db
from ..database import models
from api import schemas

router = APIRouter(prefix="/messages", tags=["messages"])

@router.post("/", response_model=schemas.MessageResponse)
async def create_message(message: schemas.MessageCreate, db: AsyncSession = Depends(get_db)):
    new_message = models.Message(
        user_id=message.user_id,
        user_message=message.user_message,
        bot_response=message.bot_response
    )
    db.add(new_message)
    await db.commit()
    await db.refresh(new_message)
    return new_message

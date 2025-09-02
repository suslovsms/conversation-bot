from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api import schemas
from ..database.database import get_db
from ..database import models

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{telegram_id}", response_model=schemas.UserOut)
async def get_user(telegram_id: str, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(models.User).where(models.User.telegram_id == telegram_id))
    user = q.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

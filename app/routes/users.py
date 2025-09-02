from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from api import schemas
from ..database.database import get_db
from ..database import models
from sqlalchemy.future import select

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.UserCreate)
async def create_user(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(models.User).where(models.User.telegram_id == user.telegram_id))
    existing = q.scalar_one_or_none()
    if existing:
        return existing
    new_user = models.User(
        telegram_id=user.telegram_id,
        chat_id=user.chat_id,
        username=user.username,
        first_name=user.first_name,
        last_name=user.last_name,
    )
    print(new_user)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

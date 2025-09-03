from api import schemas
from ..database.database import get_db
from ..database import models
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from api.schemas import UserUpdate, UserOut


router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=schemas.UserOut)
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
        gender=user.gender
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.get("/{telegram_id}", response_model=schemas.UserOut)
async def get_user(telegram_id: str, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(models.User).where(models.User.telegram_id == telegram_id))
    user = q.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{telegram_id}/gender", response_model=UserOut)
async def update_gender(telegram_id: str, data: UserUpdate, db: AsyncSession = Depends(get_db)):
    q = await db.execute(select(models.User).where(models.User.telegram_id == telegram_id))
    user = q.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.gender = data.gender
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user
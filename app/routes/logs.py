from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import models
from api import schemas
from ..database.database import get_db

router = APIRouter(prefix="/logs", tags=["logs"])

@router.post("/", response_model=schemas.LogCreate)
async def create_log(log: schemas.LogCreate, db: AsyncSession = Depends(get_db)):
    new_log = models.Log(
        user_id=log.user_id,
        level=log.level,
        source=log.source,
        message=log.message,
    )
    db.add(new_log)
    await db.commit()
    await db.refresh(new_log)
    return new_log

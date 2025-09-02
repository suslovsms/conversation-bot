from fastapi import FastAPI
from app.routes import create_user, logs, get_user
from app.database.models import Base
from app.database.database import engine

app = FastAPI(title="Astro API")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(create_user.router)
app.include_router(logs.router)
app.include_router(get_user.router)
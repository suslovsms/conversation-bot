from fastapi import FastAPI
from app.routes import users, logs
from app.database.models import Base
from app.database.database import engine

app = FastAPI(title="Astro API")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(users.router)
app.include_router(logs.router)
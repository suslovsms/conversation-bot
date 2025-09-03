from fastapi import FastAPI
from app.routes import logs, user, messages
from app.database.models import Base
from app.database.database import engine

app = FastAPI(title="Astro API")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(user.router)
app.include_router(logs.router)
app.include_router(messages.router)
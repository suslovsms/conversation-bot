import aiohttp
from datetime import datetime
from app.config import settings

async def add_logs(level, source, message, user_id=None):
    log_data = {
        "user_id": str(user_id) if user_id is not None else None,
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "source": source,
        "message": message,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{settings.API_URL}/logs/", json=log_data) as resp:
            if resp.status not in (200, 201):
                error_text = await resp.text()
                print(f"Ошибка добавления лога: {resp.status}, ответ: {error_text}")

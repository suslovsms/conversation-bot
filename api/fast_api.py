from telegram import Update
import aiohttp, traceback
from datetime import datetime
from app.config import settings

async def add_user(update: Update, user_data):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{settings.API_URL}/users", json=user_data) as resp:
            if resp.status == 200 or resp.status == 201:
                pass
            else:
                await update.message.reply_text("Error")


async def add_logs(level, source, message, user_id):
    log_data = {
        "user_id": user_id,
        "timestamp": datetime.utcnow().isoformat(),
        "level": level,
        "source": source,
        "message": message,
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{settings.API_URL}/logs", json=log_data) as resp:
                if resp.status not in (200, 201):
                    print("Ошибка добавления лога:", resp.status)
    except Exception as e:
        print("Failed to log to DB:", e)
        print(traceback.format_exc())
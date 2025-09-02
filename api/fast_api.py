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

async def check_user_exists(telegram_id: str) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{settings.API_URL}/users/{telegram_id}") as resp:
            return resp.status == 200

async def save_message(user_id: int, user_message: str, bot_response: str):
    payload = {
        "user_id": user_id,
        "user_message": user_message,
        "bot_response": bot_response
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{settings.API_URL}/messages", json=payload) as resp:
                if resp.status not in (200, 201):
                    print(f"Ошибка сохранения сообщения: {resp.status}")
    except Exception as e:
        print("Ошибка при сохранении сообщения:", e)


async def get_user_id_by_telegram_id(telegram_id: str) -> int:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{settings.API_URL}/users/{telegram_id}") as resp:
            if resp.status == 200:
                data = await resp.json()
                # безопасная проверка
                if "id" in data:
                    return data["id"]
                # debug — неожиданный формат
                print("DEBUG: /users response without id:", data)
                raise Exception("User record returned without id")
            raise Exception("User not found")
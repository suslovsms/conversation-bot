from telegram import Update
import aiohttp
from app.config import settings
from app.services.logs_service import add_logs


async def add_user(update: Update, user_data):
    async with aiohttp.ClientSession() as session:
        async with session.post(f"{settings.API_URL}/users", json=user_data) as resp:
            if resp.status in (200, 201):
                return await resp.json()
            else:
                error_text = await resp.text()
                await update.message.reply_text("Error")
                await add_logs("ERROR", "add_user", f"{resp.status}: {error_text}")


async def check_user_exists(telegram_id: str) -> bool:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{settings.API_URL}/users/{telegram_id}") as resp:
            return resp.status == 200


async def save_message(user_id: int, user_message: str, bot_response: str):
    payload = {
        "user_id": user_id,
        "user_message": user_message,
        "bot_response": bot_response,
    }
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{settings.API_URL}/messages", json=payload) as resp:
                if resp.status not in (200, 201):
                    error_text = await resp.text()
                    print(f"Ошибка сохранения сообщения: {resp.status}")
                    await add_logs("ERROR", "save_message", f"{resp.status}: {error_text}", user_id)
    except Exception as e:
        print("Ошибка при сохранении сообщения:", e)
        await add_logs("ERROR", "save_message", str(e), user_id)


async def get_user_id_by_telegram_id(telegram_id: str) -> int:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"{settings.API_URL}/users/{telegram_id}") as resp:
            if resp.status == 200:
                data = await resp.json()
                if "id" in data:
                    return data["id"]
                print("DEBUG: /users response without id:", data)
                raise Exception("User record returned without id")
            raise Exception("User not found")


async def update_gender_in_db(telegram_id: str, gender: str):
    async with aiohttp.ClientSession() as session:
        url = f"{settings.API_URL}/users/{telegram_id}/gender"
        payload = {"gender": gender}
        async with session.put(url, json=payload) as resp:
            if resp.status in (200, 201):
                return await resp.json()
            else:
                error_text = await resp.text()
                await add_logs("ERROR", "update_gender_in_db", f"{resp.status}: {error_text}")
                raise Exception(f"Ошибка обновления gender: {resp.status}, {error_text}")


async def get_user_gender(telegram_id: str) -> str | None:
    """Получить gender пользователя из API"""
    async with aiohttp.ClientSession() as session:
        url = f"{settings.API_URL}/users/{telegram_id}"
        async with session.get(url) as resp:
            if resp.status == 200:
                data = await resp.json()
                return data.get("gender")
            return None

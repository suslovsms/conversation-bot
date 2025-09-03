from telegram import Update
from telegram.ext import ContextTypes
from app.services.openai_service import generate_answer
from telegram.constants import ChatAction
from api.fast_api import get_user_id_by_telegram_id, save_message,update_gender_in_db
import asyncio

async def get_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
     user_data = {
        "telegram_id": str(update.effective_user.id),
        "username": update.effective_user.username,
        "first_name": update.effective_user.first_name,
        "last_name": update.effective_user.last_name,
        "chat_id": str(update.effective_chat.id)
        }
     return user_data


async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        chat_id = update.effective_chat.id
        text = update.message.text

        await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

        result_text = await generate_answer(text)
        await update.message.reply_text(result_text)

        user_data = await get_data(update, context)
        user_id = await get_user_id_by_telegram_id(user_data["telegram_id"])

        asyncio.create_task(save_message(user_id, text, result_text))

    except Exception as e:
        print(f"Ошибка в message_handler: {e}")
        await update.message.reply_text("Произошла ошибка. Попробуй снова.")


async def gender_btn_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("gender_"):
        try:
            gender = query.data.replace("gender_", "")
            await query.edit_message_text(text=f"Ты выбрал: {gender.capitalize()}")

            # Обновление гендера через API
            await update_gender_in_db(str(query.from_user.id), gender)

        except Exception as e:
            print(f"Ошибка в gender_btn_callback: {e}")
            await query.message.reply_text("Произошла ошибка. Попробуй снова.")




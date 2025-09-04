from telegram import Update, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from app.services.openai_service import generate_answer
from telegram.constants import ChatAction
from api.fast_api import (
    get_user_id_by_telegram_id,
    save_message,
    update_gender_in_db,
    get_user_gender,
)
import asyncio
from bot.keyboard.keyboards import keyboard
from bot.decorators.decorators import log_api_exceptions  # 👈 импортируем декоратор


async def get_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = {
        "telegram_id": str(update.effective_user.id),
        "username": update.effective_user.username,
        "first_name": update.effective_user.first_name,
        "last_name": update.effective_user.last_name,
        "chat_id": str(update.effective_chat.id),
    }
    return user_data


@log_api_exceptions("bot")  # 👈 ловим ошибки этого хендлера
async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text

    gender = context.user_data.get("gender")
    if gender is None:
        gender = await get_user_gender(str(update.effective_user.id))
        if gender:
            context.user_data["gender"] = gender

    if gender is None:
        await update.message.reply_text(
            "С кем ты желаешь пообщаться?:", reply_markup=InlineKeyboardMarkup(keyboard)
        )
        return

    await context.bot.send_chat_action(chat_id=chat_id, action=ChatAction.TYPING)

    # 👇 добавлен gender в вызов generate_answer
    result_text = await generate_answer(text, gender=gender)
    await update.message.reply_text(result_text)

    user_data = await get_data(update, context)
    user_id = await get_user_id_by_telegram_id(user_data["telegram_id"])
    asyncio.create_task(save_message(user_id, text, result_text))


@log_api_exceptions("bot")
async def gender_btn_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("gender_"):
        gender = query.data.replace("gender_", "")

        await query.edit_message_reply_markup(reply_markup=None)

        await update_gender_in_db(str(query.from_user.id), gender)

        context.user_data["gender"] = gender
        if "gender_msg_id" in context.user_data:
            context.user_data.pop("gender_msg_id")

        await query.message.reply_text("Ну что, погнали? 🚀\n\n Напиши мне что нибудь 😏")



from telegram import Update
from telegram.ext import ContextTypes
from  app.services.openai_service import generate_answer
from telegram.constants import ChatAction

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

    except Exception as e:
        print(f"Ошибка в message_handler: {e}")
        await update.message.reply_text("Произошла ошибка. Попробуй снова.")

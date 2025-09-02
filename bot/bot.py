from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from app.config import settings
from bot.bot_helper import get_data, process_message
from bot.decorators.decorators import log_command
from api.fast_api import add_user,check_user_exists


@log_command("/start")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = await get_data(update, context)
    await add_user(update, user_data)
    await update.message.reply_text("Привет! Напиши мне что-нибудь ❤️")


@log_command()
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = await get_data(update, context)

    if not await check_user_exists(user_data["telegram_id"]):
        await update.message.reply_text("Сначала нажми /start, чтобы зарегистрироваться 😊")
        return

    await process_message(update, context)


def main():
    app = ApplicationBuilder().token(settings.TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
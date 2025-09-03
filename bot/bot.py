from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters, CallbackQueryHandler
from telegram import Update, InlineKeyboardMarkup
from app.config import settings
from bot.bot_helper import get_data, process_message, gender_btn_callback
from bot.decorators.decorators import log_command
from api.fast_api import add_user, check_user_exists
from bot.keyboard.keyboards import keyboard


@log_command("/start")
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_data = await get_data(update, context)

    if await check_user_exists(user_data["telegram_id"]):
        await update.message.reply_text("Ты уже зарегистрирован 😊")
    else:
        await add_user(update, user_data)
        await update.message.reply_text("Привет! Напиши мне что-нибудь ❤️")

    await update.message.reply_text("Выбери себе персонажа:", reply_markup=InlineKeyboardMarkup(keyboard))


@log_command()
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    telegram_id = str(update.effective_user.id)

    if not await check_user_exists(telegram_id):
        await update.message.reply_text("Сначала нажми /start, чтобы зарегистрироваться 😊")
        return

    await process_message(update, context)


def main():
    app = (
        ApplicationBuilder()
        .token(settings.TELEGRAM_TOKEN)
        .read_timeout(30)  # Сколько ждать ответ от Telegram
        .write_timeout(30)  # Сколько ждать отправку сообщения
        .connect_timeout(10)  # Сколько ждать подключения
        .pool_timeout(10)  # Сколько ждать, если пул занят
        .build()
    )
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(gender_btn_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()


if __name__ == "__main__":
    main()
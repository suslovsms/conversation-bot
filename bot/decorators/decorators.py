import functools
from telegram import Update
from telegram.ext import ContextTypes
from api.fast_api import add_logs
from bot.bot_helper import get_data


def log_command(command_name: str = None):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            user_data = await get_data(update, context)
            try:
                # Если это сообщение от пользователя, логируем его текст
                log_text = command_name or update.message.text or "No message"

                await add_logs(
                    level="INFO",
                    source="bot",
                    message=f"{log_text} used",
                    user_id=user_data["telegram_id"],
                )
                return await func(update, context, *args, **kwargs)

            except Exception as e:
                await add_logs(
                    level="ERROR",
                    source="bot",
                    message=f"Error in {log_text}: {str(e)}",
                    user_id=user_data.get("telegram_id"),
                )
                await update.message.reply_text("Произошла ошибка, администратор уведомлен.")
                return None

        return wrapper

    return decorator



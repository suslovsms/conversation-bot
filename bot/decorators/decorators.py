import functools
from telegram import Update
from telegram.ext import ContextTypes
from api.fast_api import add_logs
from bot.bot_helper import get_data


def log_command(command_name: str = None):
    """
    Декоратор для логирования команд и обработки ошибок.
    Логирует:
        - INFO: успешное выполнение команды
        - ERROR: при возникновении исключения
    """
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            telegram_id = str(update.effective_user.id)
            log_text = command_name or (update.message.text if update.message else "No message")

            try:
                # Логируем факт вызова команды
                await add_logs(
                    level="INFO",
                    source="bot",
                    message=f"{log_text} used",
                    user_id=telegram_id
                )

                return await func(update, context, *args, **kwargs)

            except Exception as e:
                # Логируем ошибку
                await add_logs(
                    level="ERROR",
                    source="bot",
                    message=f"Error in {log_text}: {str(e)}",
                    user_id=telegram_id
                )

                if update.message:
                    await update.message.reply_text("Произошла ошибка, администратор уведомлен.")

                return None

        return wrapper
    return decorator

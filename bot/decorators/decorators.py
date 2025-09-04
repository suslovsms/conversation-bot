import functools
from telegram import Update
from telegram.ext import ContextTypes
from api.fast_api import get_user_id_by_telegram_id
from app.services.logs_service import add_logs
import traceback
from functools import wraps


def log_command(command_name: str = None):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
            user_id = None
            try:
                if update.effective_user:
                    telegram_id = str(update.effective_user.id)
                    try:
                        user_id = await get_user_id_by_telegram_id(telegram_id)
                    except Exception:
                        pass

                if command_name or (update.message and update.message.text.startswith("/")):
                    log_text = command_name or update.message.text
                    await add_logs(
                        level="INFO",
                        source="bot",
                        message=f"{log_text} used",
                        user_id=user_id,
                    )

                return await func(update, context, *args, **kwargs)

            except Exception as e:
                await add_logs(
                    level="ERROR",
                    source="bot",
                    message=f"Error in {command_name or 'handler'}: {str(e)}",
                    user_id=user_id,
                )
                if update.message:
                    await update.message.reply_text("Произошла ошибка, администратор уведомлен.")
                return None

        return wrapper

    return decorator


def log_api_exceptions(source: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                error_msg = "".join(traceback.format_exception(type(e), e, e.__traceback__))
                print(f"[API ERROR] {e}")
                await add_logs("ERROR", source, error_msg, kwargs.get("user_id"))
                raise
        return wrapper
    return decorator

from aiogram import Router, types, F
from aiogram.exceptions import TelegramAPIError
from utils.localization import loc
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.errors()
async def handle_errors(update: types.Update, exception: Exception) -> None:
    """
    Універсальний обробник помилок з правильним підписом параметрів
    """
    try:
        logger.error(f"Виникла помилка: {exception}")
        
        # Отримання chat_id з update, якщо можливо
        chat_id = None
        if hasattr(update, 'message') and update.message is not None:
            chat_id = update.message.chat.id
        elif hasattr(update, 'callback_query') and update.callback_query is not None:
            chat_id = update.callback_query.message.chat.id
            
        if chat_id:
            await update.bot.send_message(
                chat_id=chat_id,
                text=loc.get_message("errors.general")
            )
    except Exception as e:
        logger.error(f"Помилка в обробнику помилок: {e}")

@router.message()
async def handle_unknown_message(message: types.Message):
    """
    Обробник необроблених повідомлень
    """
    try:
        logger.info(f"Отримано необроблене повідомлення: {message.text}")
        await message.answer(
            loc.get_message("messages.unhandled_message").format(
                message=message.text
            )
        )
    except Exception as e:
        logger.error(f"Помилка обробки необробленого повідомлення: {e}")
        await message.answer(loc.get_message("errors.general"))

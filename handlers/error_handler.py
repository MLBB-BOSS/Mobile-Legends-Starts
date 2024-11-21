# File: handlers/error_handler.py

from aiogram import Router, types, F
from aiogram.exceptions import TelegramAPIError
from keyboards.main_menu import MainMenu
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.errors()
async def handle_errors(event: types.Update, exception: Exception) -> None:
    """
    Універсальний обробник помилок з правильним підписом параметрів
    """
    try:
        logger.error(f"Виникла помилка: {exception}")

        # Отримання chat_id з update, якщо можливо
        chat_id = None
        if hasattr(event, 'message') and event.message is not None:
            chat_id = event.message.chat.id
        elif hasattr(event, 'callback_query') and event.callback_query is not None:
            chat_id = event.callback_query.message.chat.id

        if chat_id:
            await event.bot.send_message(
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
        response_text = loc.get_message("messages.unhandled_message", message=message.text)
        await message.answer(
            response_text,
            reply_markup=MainMenu().get_main_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка обробки необробленого повідомлення: {e}")
        await message.answer(loc.get_message("errors.general"))

# File: handlers/error_handler.py

from aiogram import Router, types, F
from aiogram.exceptions import TelegramAPIError
from keyboards.main_menu import MainMenu
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.errors()
async def handle_errors(update: types.Update, exception: Exception) -> None:
    """
    Універсальний обробник помилок з правильним підписом параметрів
    """
    try:
        logger.error(f"Виникла помилка: {exception}")

        # Отримання chat_id з update, якщо можливо
        chat_id = None
        if isinstance(update, types.Message):
            chat_id = update.chat.id
        elif isinstance(update, types.CallbackQuery):
            chat_id = update.message.chat.id
        elif hasattr(update, 'message') and update.message:
            chat_id = update.message.chat.id
        elif hasattr(update, 'callback_query') and update.callback_query:
            chat_id = update.callback_query.message.chat.id

        if chat_id:
            error_message = loc.get_message("errors.general")
            if not error_message:  # Fallback message if localization fails
                error_message = "Виникла помилка. Будь ласка, спробуйте пізніше."
                
            await update.bot.send_message(
                chat_id=chat_id,
                text=error_message
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
        
        # Get the message with fallback
        response_text = loc.get_message("messages.unhandled_message", message=message.text)
        if not response_text:  # Fallback message if localization fails
            response_text = "Вибачте, я не розумію це повідомлення."
            
        await message.answer(
            text=response_text,
            reply_markup=MainMenu().get_main_menu()
        )
    except Exception as e:
        logger.exception(f"Помилка обробки необробленого повідомлення: {e}")
        await message.answer(
            text="Виникла помилка. Будь ласка, спробуйте пізніше."
        )

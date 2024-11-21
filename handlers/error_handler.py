# File: handlers/error_handler.py

import logging
from aiogram import Router, types, F
from aiogram.exceptions import TelegramAPIError
from keyboards.main_menu import MainMenu
from utils.localization import loc

logger = logging.getLogger(__name__)
router = Router()

@router.errors()
async def handle_errors(update: types.Update, exception: Exception) -> None:
    """
    Universal error handler with proper parameter signature
    """
    try:
        logger.error(f"Виникла помилка: {str(exception)}", exc_info=True)

        # Get chat_id from update if possible
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
            try:
                error_message = loc.get_message("errors.general")
            except Exception:
                error_message = "Виникла помилка. Будь ласка, спробуйте пізніше."
                
            await update.bot.send_message(
                chat_id=chat_id,
                text=error_message,
                reply_markup=MainMenu().get_main_menu()
            )
    except Exception as e:
        logger.error(f"Помилка в обробнику помилок: {str(e)}", exc_info=True)

@router.message()
async def handle_unknown_message(message: types.Message):
    """
    Handler for unhandled messages
    """
    try:
        logger.info(f"Отримано необроблене повідомлення: {message.text}")
        
        try:
            response_text = loc.get_message(
                "messages.unhandled_message",
                text=message.text  # Using 'text' parameter instead of 'message'
            )
        except Exception:
            response_text = f"Вибачте, я не розумію цю команду: {message.text}"
            
        await message.answer(
            text=response_text,
            reply_markup=MainMenu().get_main_menu()
        )
        
    except Exception as e:
        logger.error(f"Помилка обробки необробленого повідомлення: {str(e)}", exc_info=True)
        try:
            error_message = loc.get_message("errors.general")
        except Exception:
            error_message = "Виникла помилка. Будь ласка, спробуйте пізніше."
        
        await message.answer(
            text=error_message,
            reply_markup=MainMenu().get_main_menu()
        )

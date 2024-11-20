# handlers/message_handlers.py
from aiogram import Router, types, F
from aiogram.exceptions import TelegramAPIError
from utils.localization import loc
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.errors()
async def handle_errors(event: types.ErrorEvent, exception: Exception) -> None:
    """
    Universal error handler
    """
    try:
        logger.error(f"Error occurred: {exception}")
        
        if isinstance(exception, TelegramAPIError):
            # Handle Telegram API errors
            error_message = loc.get_message("errors.general")
        else:
            # Handle other errors
            error_message = loc.get_message("errors.general")
        
        # Try to get the chat_id from the update object
        if hasattr(event, 'update') and hasattr(event.update, 'message'):
            chat_id = event.update.message.chat.id
            await event.update.bot.send_message(
                chat_id=chat_id,
                text=error_message
            )
    except Exception as e:
        logger.error(f"Error in error handler: {e}")

# Handle unhandled messages
@router.message()
async def handle_unknown_message(message: types.Message):
    """
    Handler for messages that weren't caught by other handlers
    """
    try:
        logger.info(f"Unhandled message received: {message.text}")
        await message.answer(
            loc.get_message("messages.unhandled_message").format(
                message=message.text
            )
        )
    except Exception as e:
        logger.error(f"Error handling unknown message: {e}")
        await message.answer(loc.get_message("errors.general"))

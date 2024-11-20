# handlers/message_handlers.py
from aiogram import Router, types, F
from aiogram.exceptions import TelegramAPIError
from utils.localization import loc
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.errors()
async def handle_errors(update: types.Update, exception: Exception) -> None:
    """
    Universal error handler with correct parameter signature
    """
    try:
        logger.error(f"Exception occurred: {exception}")
        
        # Get chat_id from update if possible
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
        logger.error(f"Error in error handler: {e}")

@router.message()
async def handle_unknown_message(message: types.Message):
    """
    Handler for unhandled messages
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

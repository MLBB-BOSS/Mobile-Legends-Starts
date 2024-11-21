# File: handlers/error_handler.py

from aiogram import Router, types
from aiogram.filters import ExceptionTypeFilter
import logging
from utils.localization import loc

logger = logging.getLogger(__name__)
router = Router()

@router.errors()
async def handle_error(update: types.Update, exception: Exception) -> bool:
    """Handle all errors that occur during message processing"""
    try:
        logger.error(f"Error handling update {update.update_id}: {exception}", exc_info=True)
        
        # Get the message object if available
        message = update.message or update.callback_query.message if update.callback_query else None
        
        if message:
            error_text = loc.get_message("errors.general")
            await message.answer(error_text)
        
        # Return True to indicate that the error was handled
        return True
        
    except Exception as e:
        logger.error(f"Error in error handler: {e}", exc_info=True)
        return False

@router.message()
async def handle_unknown_message(message: types.Message):
    """Handle any message that wasn't caught by other handlers"""
    try:
        logger.info(f"Received unhandled message: {message.text}")
        response_text = loc.get_message(
            "messages.unhandled_message",
            message_text=message.text
        )
        await message.answer(response_text)
    except Exception as e:
        logger.error(f"Error handling unknown message: {e}", exc_info=True)
        await message.answer(loc.get_message("errors.general"))

from typing import Optional
import logging
from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramAPIError, TelegramBadRequest

logger = logging.getLogger(__name__)

async def safe_delete_message(bot: Bot, chat_id: int, message_id: Optional[int]) -> bool:
    if not message_id:
        return False
        
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
        logger.info(f"Successfully deleted message {message_id} in chat {chat_id}")
        return True
    except TelegramAPIError as e:
        logger.error(f"Failed to delete message {message_id} in chat {chat_id}: {e}")
        return False

async def check_and_edit_message(
    bot: Bot,
    chat_id: int,
    message_id: Optional[int],
    text: str,
    keyboard: Optional[InlineKeyboardMarkup] = None,
    parse_mode: ParseMode = ParseMode.HTML
) -> bool:
    if not message_id:
        return False
        
    try:
        await bot.edit_message_text(
            text=text,
            chat_id=chat_id,
            message_id=message_id,
            reply_markup=keyboard,
            parse_mode=parse_mode
        )
        logger.info(f"Successfully edited message {message_id} in chat {chat_id}")
        return True
    except TelegramBadRequest as e:
        logger.warning(f"Cannot edit message {message_id}: {e}")
        return False
    except TelegramAPIError as e:
        logger.error(f"Error editing message {message_id}: {e}")
        return False

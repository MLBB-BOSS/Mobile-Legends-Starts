# utils/message_utils.py
from typing import Optional, Union, Dict, Any
import logging
from aiogram import Bot
from aiogram.types import (
    Message,
    InlineKeyboardMarkup,
    CallbackQuery,
    InputFile,
    InputMediaPhoto
)
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramAPIError, TelegramBadRequest

# Configure logging
logger = logging.getLogger(__name__)

async def safe_delete_message(
    bot: Bot,
    chat_id: int,
    message_id: Optional[int]
) -> bool:
    """
    Safely delete a message
    
    Args:
        bot: Bot instance
        chat_id: Chat ID
        message_id: Message ID
        
    Returns:
        bool: Success status
    """
    if not message_id:
        return False
        
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
        logger.info(f"Deleted message {message_id} in chat {chat_id}")
        return True
    except TelegramAPIError as e:
        logger.error(f"Cannot delete message {message_id}: {e}")
        return False

async def edit_or_send_message(
    bot: Bot,
    chat_id: int,
    text: str,
    message_id: Optional[int] = None,
    keyboard: Optional[InlineKeyboardMarkup] = None,
    parse_mode: ParseMode = ParseMode.HTML,
    **kwargs: Any
) -> Optional[Message]:
    """Edit existing message or send new one"""
    try:
        if message_id:
            try:
                return await bot.edit_message_text(
                    text=text,
                    chat_id=chat_id,
                    message_id=message_id,
                    reply_markup=keyboard,
                    parse_mode=parse_mode
                )
            except TelegramBadRequest:
                await safe_delete_message(bot, chat_id, message_id)
        
        return await bot.send_message(
            chat_id=chat_id,
            text=text,
            reply_markup=keyboard,
            parse_mode=parse_mode,
            **kwargs
        )
        
    except Exception as e:
        logger.error(f"Error in edit_or_send_message: {e}")
        return None

class MessageManager:
    """Manager for message operations"""
    
    def __init__(self, bot: Bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    async def send_or_edit(
        self,
        chat_id: int,
        text: str,
        message_id: Optional[int] = None,
        keyboard: Optional[InlineKeyboardMarkup] = None,
        parse_mode: ParseMode = ParseMode.HTML,
        **kwargs: Any
    ) -> Optional[Message]:
        """Send new message or edit existing one"""
        return await edit_or_send_message(
            self.bot,
            chat_id,
            text,
            message_id,
            keyboard,
            parse_mode,
            **kwargs
        )

    async def safe_delete(
        self,
        chat_id: int,
        message_id: Optional[int]
    ) -> bool:
        """Safely delete a message"""
        return await safe_delete_message(self.bot, chat_id, message_id)

# Експортуємо всі необхідні функції та класи
__all__ = [
    'MessageManager',
    'safe_delete_message',
    'edit_or_send_message'
]

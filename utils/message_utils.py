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
        try:
            if message_id:
                try:
                    return await self.bot.edit_message_text(
                        text=text,
                        chat_id=chat_id,
                        message_id=message_id,
                        reply_markup=keyboard,
                        parse_mode=parse_mode
                    )
                except TelegramBadRequest:
                    await self.safe_delete_message(chat_id, message_id)
            
            return await self.bot.send_message(
                chat_id=chat_id,
                text=text,
                reply_markup=keyboard,
                parse_mode=parse_mode,
                **kwargs
            )
        except Exception as e:
            self.logger.error(f"Error in send_or_edit: {e}")
            return None

    async def safe_delete_message(
        self,
        chat_id: int,
        message_id: Optional[int]
    ) -> bool:
        """Safely delete a message"""
        if not message_id:
            return False
            
        try:
            await self.bot.delete_message(
                chat_id=chat_id,
                message_id=message_id
            )
            return True
        except TelegramAPIError as e:
            self.logger.warning(f"Cannot delete message {message_id}: {e}")
            return False

    async def update_media_message(
        self,
        chat_id: int,
        message_id: int,
        photo: Union[InputFile, str],
        caption: Optional[str] = None,
        keyboard: Optional[InlineKeyboardMarkup] = None
    ) -> bool:
        """Update media message"""
        try:
            await self.bot.edit_message_media(
                chat_id=chat_id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=photo,
                    caption=caption,
                    parse_mode=ParseMode.HTML
                ),
                reply_markup=keyboard
            )
            return True
        except TelegramAPIError as e:
            self.logger.error(f"Error updating media message: {e}")
            return False

# Create __all__ for explicit exports
__all__ = ['MessageManager']

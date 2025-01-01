# utils/message_utils.py
from typing import Optional, Union, Dict, Any
import logging
from aiogram import Bot
from aiogram.types import (
    InlineKeyboardMarkup,
    Message,
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
        self.logger = logger

    async def send_or_edit(
        self,
        chat_id: int,
        text: str,
        message_id: Optional[int] = None,
        keyboard: Optional[InlineKeyboardMarkup] = None,
        parse_mode: ParseMode = ParseMode.HTML,
        **kwargs: Any
    ) -> Optional[Message]:
        """
        Send new message or edit existing one
        
        Args:
            chat_id: Chat ID
            text: Message text
            message_id: Existing message ID to edit
            keyboard: Optional inline keyboard
            parse_mode: Message parse mode
            **kwargs: Additional parameters for send_message
            
        Returns:
            Optional[Message]: New or edited message
        """
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
                    # If can't edit, send new message
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
        """
        Safely delete a message
        
        Args:
            chat_id: Chat ID
            message_id: Message ID
            
        Returns:
            bool: Success status
        """
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
        media: Union[InputFile, str],
        caption: Optional[str] = None,
        keyboard: Optional[InlineKeyboardMarkup] = None,
        parse_mode: ParseMode = ParseMode.HTML
    ) -> bool:
        """
        Update media message with new media/caption
        
        Args:
            chat_id: Chat ID
            message_id: Message ID
            media: New media (file or file_id)
            caption: New caption
            keyboard: New keyboard
            parse_mode: Parse mode
            
        Returns:
            bool: Success status
        """
        try:
            await self.bot.edit_message_media(
                chat_id=chat_id,
                message_id=message_id,
                media=InputMediaPhoto(
                    media=media,
                    caption=caption,
                    parse_mode=parse_mode
                ),
                reply_markup=keyboard
            )
            return True
        except TelegramAPIError as e:
            self.logger.error(f"Error updating media message: {e}")
            return False

    @staticmethod
    async def answer_callback(
        callback: CallbackQuery,
        text: Optional[str] = None,
        show_alert: bool = False
    ) -> bool:
        """
        Safely answer callback query
        
        Args:
            callback: Callback query
            text: Answer text
            show_alert: Show as alert
            
        Returns:
            bool: Success status
        """
        try:
            await callback.answer(text, show_alert=show_alert)
            return True
        except TelegramAPIError as e:
            logger.error(f"Error answering callback: {e}")
            return False

# Standalone functions
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
    """
    Edit existing message or send new one
    
    Args:
        bot: Bot instance
        chat_id: Chat ID
        text: Message text
        message_id: Existing message ID
        keyboard: Optional keyboard
        parse_mode: Parse mode
        **kwargs: Additional parameters
        
    Returns:
        Optional[Message]: Edited or new message
    """
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

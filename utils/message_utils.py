"""
Utility module for handling Telegram bot messages.
Provides safe operations for message manipulation and error handling.
"""

from typing import Optional, List, NoReturn
import logging
from dataclasses import dataclass
from enum import Enum

from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, Message
from aiogram.enums import ParseMode
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramAPIError, TelegramBadRequest  # Updated imports

# Configure logging
logger = logging.getLogger(__name__)

class MessageOperationError(Exception):
    """Base exception for message operations."""
    pass

class MessageHandlingResult(Enum):
    """Enum for message handling operation results."""
    SUCCESS = "success"
    FAILED = "failed"
    PARTIAL = "partial"

@dataclass
class MessageContext:
    """Data class for message context."""
    chat_id: int
    message_id: Optional[int]
    text: str
    keyboard: Optional[InlineKeyboardMarkup] = None
    parse_mode: ParseMode = ParseMode.HTML

class MessageHandler:
    """Class for handling message operations."""
    
    def __init__(self, bot: Bot):
        self.bot = bot
        
    async def safe_delete_message(self, chat_id: int, message_id: int) -> bool:
        """
        Safely delete a message.
        
        Args:
            chat_id: The chat ID where the message is located
            message_id: The ID of the message to delete
            
        Returns:
            bool: True if deletion was successful, False otherwise
        """
        try:
            await self.bot.delete_message(chat_id=chat_id, message_id=message_id)
            logger.info("Deleted message %d in chat %d", message_id, chat_id)
            return True
        except TelegramAPIError as e:
            logger.error("Failed to delete message %d in chat %d: %s", 
                        message_id, chat_id, str(e))
            return False

    async def check_and_edit_message(
        self,
        context: MessageContext,
        state: FSMContext
    ) -> MessageHandlingResult:
        """
        Check and edit an existing message.
        
        Args:
            context: MessageContext instance containing message details
            state: FSM context for state management
            
        Returns:
            MessageHandlingResult: Result of the operation
            
        Raises:
            MessageOperationError: If message editing fails
        """
        try:
            await self.bot.edit_message_text(
                chat_id=context.chat_id,
                message_id=context.message_id,
                text=context.text,
                reply_markup=context.keyboard,
                parse_mode=context.parse_mode
            )
            logger.info("Edited message %d in chat %d", 
                       context.message_id, context.chat_id)
            return MessageHandlingResult.SUCCESS
        except TelegramBadRequest as e:
            # Handle both message not found and can't be edited cases
            logger.warning("Cannot edit message %d: %s", 
                         context.message_id, str(e))
            return MessageHandlingResult.FAILED
        except TelegramAPIError as e:
            logger.error("Error editing message %d: %s", 
                        context.message_id, str(e))
            raise MessageOperationError(f"Failed to edit message: {str(e)}")

    # Rest of the code remains the same...

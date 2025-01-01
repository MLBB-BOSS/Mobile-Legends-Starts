# handlers/interface_manager.py
from dataclasses import dataclass
from typing import Optional, Tuple
from aiogram import Bot
from aiogram.types import Message, ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramAPIError
from logging import getLogger

logger = getLogger(__name__)

@dataclass
class InterfaceState:
    """Current interface state"""
    control_message_id: Optional[int] = None
    screen_message_id: Optional[int] = None
    last_control_text: Optional[str] = None
    last_screen_text: Optional[str] = None
    last_control_markup: Optional[ReplyKeyboardMarkup] = None
    last_screen_markup: Optional[InlineKeyboardMarkup] = None

class InterfaceManager:
    """Manager for two-component interface (control panel and screen)"""
    
    def __init__(self, bot: Bot, chat_id: int, state: FSMContext):
        self.bot = bot
        self.chat_id = chat_id
        self.state = state
        self.logger = getLogger(__name__)

    async def load_state(self) -> InterfaceState:
        """Load interface state from FSM"""
        try:
            data = await self.state.get_data()
            return InterfaceState(
                control_message_id=data.get('control_message_id'),
                screen_message_id=data.get('screen_message_id'),
                last_control_text=data.get('last_control_text'),
                last_screen_text=data.get('last_screen_text'),
                last_control_markup=data.get('last_control_markup'),
                last_screen_markup=data.get('last_screen_markup')
            )
        except Exception as e:
            self.logger.error(f"Error loading interface state: {e}")
            return InterfaceState()

    async def update_interface(
        self,
        control_text: str,
        control_markup: ReplyKeyboardMarkup,
        screen_text: str,
        screen_markup: InlineKeyboardMarkup
    ) -> Tuple[int, int]:
        """Update both control panel and screen"""
        try:
            current_state = await self.load_state()
            
            # Update control panel
            if current_state.control_message_id:
                await self.bot.delete_message(
                    self.chat_id,
                    current_state.control_message_id
                )
            
            control_message = await self.bot.send_message(
                chat_id=self.chat_id,
                text=control_text,
                reply_markup=control_markup
            )
            
            # Update screen
            if current_state.screen_message_id:
                screen_message = await self.bot.edit_message_text(
                    text=screen_text,
                    chat_id=self.chat_id,
                    message_id=current_state.screen_message_id,
                    reply_markup=screen_markup
                )
            else:
                screen_message = await self.bot.send_message(
                    chat_id=self.chat_id,
                    text=screen_text,
                    reply_markup=screen_markup
                )
            
            # Save new state
            await self.state.update_data(
                control_message_id=control_message.message_id,
                screen_message_id=screen_message.message_id,
                last_control_text=control_text,
                last_screen_text=screen_text,
                last_control_markup=control_markup,
                last_screen_markup=screen_markup
            )
            
            return control_message.message_id, screen_message.message_id
            
        except TelegramAPIError as e:
            self.logger.error(f"Telegram API error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Error updating interface: {e}")
            raise

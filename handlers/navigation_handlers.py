from typing import Optional, Dict, Any
from aiogram import Router, Bot, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import ReplyKeyboardMarkup, InlineKeyboardMarkup
import logging
from dataclasses import dataclass

from states.menu_states import NavigationState, MainMenuState
from keyboards.menus import get_navigation_menu
from utils.message_utils import safe_delete_message

logger = logging.getLogger(__name__)

@dataclass
class NavigationMessages:
    """Navigation interface messages"""
    MAIN_SCREEN: str = "🧭 Навігаційне меню"
    HERO_SELECT: str = "Оберіть героя для перегляду"
    ERROR: str = "Сталася помилка. Спробуйте ще раз."
    UNKNOWN_COMMAND: str = "Невідома команда. Будь ласка, використовуйте кнопки меню."

class NavigationHandler:
    """Handler for navigation section"""

    def __init__(self) -> None:
        """Initialize navigation handler"""
        self.router = Router(name='navigation')
        self._setup_router()

    def _setup_router(self) -> None:
        """Configure router with handlers"""
        # Message handlers
        self.router.message.register(
            self._handle_navigation_start,
            F.text == "🧭 Навігація",
            MainMenuState.main
        )
        
        self.router.message.register(
            self._handle_navigation_menu,
            NavigationState.main
        )

    async def _handle_navigation_start(
        self,
        message: Message,
        state: FSMContext,
        bot: Bot
    ) -> None:
        """
        Handle transition to navigation menu
        
        Args:
            message: User's message
            state: FSM context
            bot: Bot instance
        """
        try:
            # Delete user's message
            await safe_delete_message(bot, message.chat.id, message.message_id)
            
            # Get current interface state
            data = await state.get_data()
            current_message_id = data.get('bot_message_id')
            
            # Delete previous bot message if exists
            if current_message_id:
                await safe_delete_message(
                    bot,
                    message.chat.id,
                    current_message_id
                )
            
            # Send new navigation menu
            new_message = await bot.send_message(
                chat_id=message.chat.id,
                text=NavigationMessages.MAIN_SCREEN,
                reply_markup=get_navigation_menu()
            )
            
            # Update state
            await state.set_state(NavigationState.main)
            await state.update_data(bot_message_id=new_message.message_id)
            
            logger.info(
                f"User {message.from_user.id} entered navigation menu"
            )
            
        except Exception as e:
            logger.error(
                f"Error in navigation start handler for user {message.from_user.id}: {e}"
            )
            await self._handle_error(message, bot)

    async def _handle_navigation_menu(
        self,
        message: Message,
        state: FSMContext,
        bot: Bot
    ) -> None:
        """
        Handle navigation menu choices
        
        Args:
            message: User's message
            state: FSM context
            bot: Bot instance
        """
        try:
            # Delete user's message
            await safe_delete_message(bot, message.chat.id, message.message_id)
            
            # Get current state data
            data = await state.get_data()
            current_message_id = data.get('bot_message_id')
            
            match message.text:
                case "🔍 Обрати героя":
                    await self._show_hero_selection(
                        message=message,
                        state=state,
                        bot=bot,
                        current_message_id=current_message_id
                    )
                case "🔙 Назад":
                    await self._back_to_main_menu(
                        message=message,
                        state=state,
                        bot=bot,
                        current_message_id=current_message_id
                    )
                case _:
                    await self._handle_unknown_command(message, bot)
            
        except Exception as e:
            logger.error(
                f"Error in navigation menu handler for user {message.from_user.id}: {e}"
            )
            await self._handle_error(message, bot)

    async def _show_hero_selection(
        self,
        message: Message,
        state: FSMContext,
        bot: Bot,
        current_message_id: Optional[int]
    ) -> None:
        """
        Show hero selection menu
        
        Args:
            message: User's message
            state: FSM context
            bot: Bot instance
            current_message_id: ID of current bot message
        """
        try:
            # Delete previous message
            if current_message_id:
                await safe_delete_message(
                    bot,
                    message.chat.id,
                    current_message_id
                )
            
            # Send hero selection menu
            new_message = await bot.send_message(
                chat_id=message.chat.id,
                text=NavigationMessages.HERO_SELECT,
                reply_markup=get_navigation_menu()  # You might want to create a specific hero selection keyboard
            )
            
            # Update state
            await state.set_state(NavigationState.select_hero)
            await state.update_data(bot_message_id=new_message.message_id)
            
        except Exception as e:
            logger.error(
                f"Error showing hero selection for user {message.from_user.id}: {e}"
            )
            raise

    async def _back_to_main_menu(
        self,
        message: Message,
        state: FSMContext,
        bot: Bot,
        current_message_id: Optional[int]
    ) -> None:
        """
        Return to main menu
        
        Args:
            message: User's message
            state: FSM context
            bot: Bot instance
            current_message_id: ID of current bot message
        """
        try:
            # Delete current message
            if current_message_id:
                await safe_delete_message(
                    bot,
                    message.chat.id,
                    current_message_id
                )
            
            # Send main menu
            new_message = await bot.send_message(
                chat_id=message.chat.id,
                text="🏠 Головне меню",
                reply_markup=get_navigation_menu()  # You should create get_main_menu function
            )
            
            # Update state
            await state.set_state(MainMenuState.main)
            await state.update_data(bot_message_id=new_message.message_id)
            
        except Exception as e:
            logger.error(
                f"Error returning to main menu for user {message.from_user.id}: {e}"
            )
            raise

    async def _handle_unknown_command(
        self,
        message: Message,
        bot: Bot
    ) -> None:
        """
        Handle unknown command
        
        Args:
            message: User's message
            bot: Bot instance
        """
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text=NavigationMessages.UNKNOWN_COMMAND,
                reply_markup=get_navigation_menu()
            )
        except Exception as e:
            logger.error(
                f"Error handling unknown command for user {message.from_user.id}: {e}"
            )
            raise

    async def _handle_error(
        self,
        message: Message,
        bot: Bot
    ) -> None:
        """
        Handle errors in navigation handler
        
        Args:
            message: User's message
            bot: Bot instance
        """
        try:
            await bot.send_message(
                chat_id=message.chat.id,
                text=NavigationMessages.ERROR,
                reply_markup=get_navigation_menu()
            )
        except Exception as e:
            logger.critical(
                f"Failed to handle error for user {message.from_user.id}: {e}"
            )

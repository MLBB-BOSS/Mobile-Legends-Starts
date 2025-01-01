from typing import Optional, Any, Dict, Tuple
from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramAPIError
from aiogram.utils.keyboard import ReplyKeyboardMarkup, InlineKeyboardMarkup
from dataclasses import dataclass
from logging import getLogger
from enum import Enum, auto

from states.menu_states import NavigationState, MainMenuState, MenuStates
from keyboards.menus import get_navigation_menu, get_main_menu_inline
from utils.message_utils import safe_delete_message

# Constants and Configurations
class NavigationCallback(str, Enum):
    """Navigation callback data"""
    HERO_SELECT = "nav_hero_select"
    HERO_DETAILS = "nav_hero_details"
    BACK = "nav_back"
    MAIN_MENU = "nav_main"

@dataclass
class NavigationTexts:
    """Navigation menu texts"""
    MAIN_SCREEN = "🧭 Навігація по грі"
    HERO_SELECT = "Оберіть героя:"
    HERO_DETAILS = "Інформація про героя:"
    ERROR = "Виникла помилка. Спробуйте ще раз."
    UNKNOWN_COMMAND = "Невідома команда. Оберіть опцію з меню."

class NavigationMenuOptions(str, Enum):
    """Navigation menu options"""
    HEROES = "🥷 Персонажі"
    TOURNAMENTS = "🏆 Турніри"
    GUIDES = "📚 Гайди"
    BUILDS = "🛡️ Білди"
    TEAMS = "🧑‍🤝‍🧑 Команди"
    CHALLENGES = "🧩 Челендж"
    BOOST = "🚀 Буст"
    TRADING = "💰 Торгівля"
    BACK = "🔙 Назад"

class NavigationHandler:
    """Handler for navigation section"""

    def __init__(self) -> None:
        """Initialize navigation handler"""
        self.router = Router(name="navigation")
        self.logger = getLogger("handlers.navigation")
        self._setup_router()

    def _setup_router(self) -> None:
        """Setup router with handlers"""
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
        
        # Callback handlers
        self.router.callback_query.register(
            self._handle_hero_select,
            F.data == NavigationCallback.HERO_SELECT
        )
        
        self.router.callback_query.register(
            self._handle_back_to_main,
            F.data == NavigationCallback.BACK
        )

    async def _update_interface_messages(
        self,
        bot: Bot,
        chat_id: int,
        old_message_id: Optional[int],
        interactive_message_id: Optional[int],
        state: FSMContext
    ) -> Tuple[Optional[int], Optional[int]]:
        """
        Update interface messages
        
        Args:
            bot: Bot instance
            chat_id: Chat ID
            old_message_id: ID of old message to delete
            interactive_message_id: ID of old interactive message
            state: FSM context
        
        Returns:
            Tuple[Optional[int], Optional[int]]: New message IDs
        """
        try:
            # Delete old messages
            if old_message_id:
                await safe_delete_message(bot, chat_id, old_message_id)
            if interactive_message_id:
                await safe_delete_message(bot, chat_id, interactive_message_id)

            # Create new message
            new_message = await bot.send_message(
                chat_id=chat_id,
                text=NavigationTexts.MAIN_SCREEN,
                reply_markup=get_navigation_menu()
            )

            return new_message.message_id, new_message.message_id
        except Exception as e:
            self.logger.error(f"Error updating interface: {e}")
            return None, None

    async def _handle_navigation_start(
        self,
        message: Message,
        state: FSMContext,
        bot: Bot
    ) -> None:
        """Handle transition to navigation menu"""
        try:
            await safe_delete_message(bot, message.chat.id, message.message_id)
            
            data = await state.get_data()
            
            new_message_id, new_interactive_id = await self._update_interface_messages(
                bot=bot,
                chat_id=message.chat.id,
                old_message_id=data.get('bot_message_id'),
                interactive_message_id=data.get('interactive_message_id'),
                state=state
            )

            if new_message_id and new_interactive_id:
                await state.update_data(
                    bot_message_id=new_message_id,
                    interactive_message_id=new_interactive_id
                )
                await state.set_state(NavigationState.main)
                self.logger.info(f"User {message.from_user.id} entered navigation menu")
            else:
                raise ValueError("Failed to update interface")

        except Exception as e:
            self.logger.error(f"Error in navigation start: {e}")
            await self._handle_error(bot, message.chat.id, message.from_user.id)

    async def _handle_navigation_menu(
        self,
        message: Message,
        state: FSMContext,
        bot: Bot
    ) -> None:
        """Handle navigation menu choices"""
        try:
            text = message.text
            await safe_delete_message(bot, message.chat.id, message.message_id)

            # Mapping menu options to states
            menu_states = {
                NavigationMenuOptions.HEROES: MenuStates.HEROES_MENU,
                NavigationMenuOptions.TOURNAMENTS: MenuStates.TOURNAMENTS_MENU,
                NavigationMenuOptions.GUIDES: MenuStates.GUIDES_MENU,
                NavigationMenuOptions.BUILDS: MenuStates.BUILDS_MENU,
                NavigationMenuOptions.TEAMS: MenuStates.TEAMS_MENU,
                NavigationMenuOptions.CHALLENGES: MenuStates.CHALLENGES_MENU,
                NavigationMenuOptions.BOOST: MenuStates.BUST_MENU,
                NavigationMenuOptions.TRADING: MenuStates.TRADING_MENU,
                NavigationMenuOptions.BACK: MenuStates.MAIN_MENU
            }

            if text in [option.value for option in NavigationMenuOptions]:
                selected_option = NavigationMenuOptions(text)
                new_state = menu_states[selected_option]
                
                await self._update_state_and_interface(
                    bot=bot,
                    chat_id=message.chat.id,
                    state=state,
                    new_state=new_state,
                    text=f"Ви перейшли до розділу {text}"
                )
            else:
                await self._handle_unknown_command(bot, message.chat.id)

        except Exception as e:
            self.logger.error(f"Error in navigation menu: {e}")
            await self._handle_error(bot, message.chat.id, message.from_user.id)

    async def _update_state_and_interface(
        self,
        bot: Bot,
        chat_id: int,
        state: FSMContext,
        new_state: MenuStates,
        text: str
    ) -> None:
        """Update state and interface"""
        try:
            data = await state.get_data()
            new_message_id, new_interactive_id = await self._update_interface_messages(
                bot=bot,
                chat_id=chat_id,
                old_message_id=data.get('bot_message_id'),
                interactive_message_id=data.get('interactive_message_id'),
                state=state
            )

            if new_message_id and new_interactive_id:
                await state.set_state(new_state)
                await state.update_data(
                    bot_message_id=new_message_id,
                    interactive_message_id=new_interactive_id
                )
                self.logger.info(f"Updated state to {new_state}")
            else:
                raise ValueError("Failed to update interface")

        except Exception as e:
            self.logger.error(f"Error updating state and interface: {e}")
            raise

    async def _handle_error(
        self,
        bot: Bot,
        chat_id: int,
        user_id: int,
        error: Optional[Exception] = None
    ) -> None:
        """Handle errors in navigation"""
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=NavigationTexts.ERROR,
                reply_markup=get_navigation_menu()
            )
            self.logger.error(f"Error for user {user_id}: {error if error else 'Unknown error'}")
        except Exception as e:
            self.logger.critical(f"Failed to handle error for user {user_id}: {e}")

    async def _handle_unknown_command(
        self,
        bot: Bot,
        chat_id: int
    ) -> None:
        """Handle unknown commands"""
        try:
            await bot.send_message(
                chat_id=chat_id,
                text=NavigationTexts.UNKNOWN_COMMAND,
                reply_markup=get_navigation_menu()
            )
        except Exception as e:
            self.logger.error(f"Error handling unknown command: {e}")
            raise

# Create router instance
navigation_router = NavigationHandler().router

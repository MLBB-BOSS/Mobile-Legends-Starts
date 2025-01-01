# handlers/navigation.py
from typing import Optional, Any, Dict
from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramAPIError
from aiogram.utils.keyboard import ReplyKeyboardMarkup, InlineKeyboardMarkup
from dataclasses import dataclass
from logging import getLogger
from enum import Enum, auto

from states.menu_states import NavigationState, MainMenuState
from keyboards.menus import get_navigation_menu, get_main_menu_inline
from utils.message_utils import safe_delete_message

# Constants
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
            F.data == NavigationCallback.HERO_SELECT,
            NavigationState.main
        )
        
        self.router.callback_query.register(
            self._handle_back_to_main,
            F.data == NavigationCallback.BACK
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
            
            # Update interface with navigation menu
            await self._update_interface(
                bot=bot,
                chat_id=message.chat.id,
                state=state,
                text=NavigationTexts.MAIN_SCREEN,
                keyboard=get_navigation_menu(),
                current_data=data
            )
            
            # Set navigation state
            await state.set_state(NavigationState.main)
            self.logger.info(f"User {message.from_user.id} entered navigation menu")
            
        except Exception as e:
            await self._handle_error(
                bot=bot,
                chat_id=message.chat.id,
                user_id=message.from_user.id,
                error=e
            )

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
            user_choice = message.text
            await safe_delete_message(bot, message.chat.id, message.message_id)
            
            data = await state.get_data()
            
            match user_choice:
                case "🔍 Обрати героя":
                    await self._show_hero_selection(bot, message.chat.id, state, data)
                case "🔙 Назад":
                    await self._back_to_main_menu(bot, message.chat.id, state, data)
                case _:
                    await self._handle_unknown_command(bot, message.chat.id, state, data)
                    
        except Exception as e:
            await self._handle_error(
                bot=bot,
                chat_id=message.chat.id,
                user_id=message.from_user.id,
                error=e
            )

    async def _update_interface(
        self,
        bot: Bot,
        chat_id: int,
        state: FSMContext,
        text: str,
        keyboard: ReplyKeyboardMarkup | InlineKeyboardMarkup,
        current_data: Dict[str, Any]
    ) -> None:
        """
        Update interface with new message and keyboard
        
        Args:
            bot: Bot instance
            chat_id: Chat ID
            state: FSM context
            text: New message text
            keyboard: New keyboard
            current_data: Current state data
        """
        try:
            # Delete old message if exists
            old_message_id = current_data.get('bot_message_id')
            if old_message_id:
                await safe_delete_message(bot, chat_id, old_message_i 

router = Router()
logger = logging.getLogger(__name__)

async def update_interface_messages(bot: Bot, chat_id: int, old_message_id: int, 
                                 interactive_message_id: int, state: FSMContext) -> tuple[int, int]:
    """Оновлює інтерфейсні повідомлення."""
    try:
        # Видаляємо старі повідомлення
        if old_message_id:
            await safe_delete_message(bot, chat_id, old_message_id)
        if interactive_message_id:
            await safe_delete_message(bot, chat_id, interactive_message_id)

        # Створюємо нове повідомлення
        new_message = await bot.send_message(
            chat_id=chat_id,
            text=NavigationConfig.Messages.NAVIGATION_MENU,
            reply_markup=get_navigation_menu()
        )

        return new_message.message_id, new_message.message_id
    except Exception as e:
        logger.error(f"Помилка при оновленні інтерфейсу: {e}")
        return None, None

async def handle_navigation_error(bot: Bot, chat_id: int, state: FSMContext):
    """Обробляє помилки навігації."""
    try:
        await bot.send_message(
            chat_id=chat_id,
            text="Виникла помилка при навігації. Спробуйте ще раз або зверніться до адміністратора.",
            reply_markup=get_navigation_menu()
        )
        await state.set_state(MenuStates.MAIN_MENU)
    except Exception as e:
        logger.error(f"Помилка при обробці помилки навігації: {e}")

@router.message(MenuStates.MAIN_MENU, F.text == "🧭 Навігація")
async def handle_navigation_transition(message: Message, state: FSMContext, bot: Bot):
    """Обробник переходу до навігаційного меню."""
    logger.info(f"Користувач {message.from_user.id} перейшов до навігаційного меню")
    
    # Ініціалізація менеджера станів
    state_manager = NavigationStateManager(state)
    await state_manager.load_state()

    try:
        # Видалення повідомлення користувача
        if not await safe_delete_message(bot, message.chat.id, message.message_id):
            logger.warning(f"Не вдалося видалити повідомлення користувача {message.message_id}")

        # Оновлення інтерфейсу
        new_message_id, new_interactive_id = await update_interface_messages(
            bot=bot,
            chat_id=message.chat.id,
            old_message_id=state_manager.messages.bot_message_id,
            interactive_message_id=state_manager.messages.interactive_message_id,
            state=state
        )

        if new_message_id and new_interactive_id:
            # Оновлення даних повідомлень
            await state_manager.messages.update(
                bot=bot,
                chat_id=message.chat.id,
                new_message_id=new_message_id,
                new_interactive_id=new_interactive_id,
                text=NavigationConfig.Messages.NAVIGATION_MENU,
                keyboard=get_navigation_menu()
            )
            
            # Перехід до нового стану
            await state_manager.transition_to(MenuStates.NAVIGATION_MENU)
            logger.info(f"Успішний перехід до навігаційного меню для користувача {message.from_user.id}")
        else:
            raise ValueError("Не вдалося оновити інтерфейс")

    except Exception as e:
        logger.error(f"Помилка при переході до навігаційного меню: {e}")
        await handle_navigation_error(bot, message.chat.id, state)

# Додамо обробники для підменю навігації
@router.message(MenuStates.NAVIGATION_MENU)
async def handle_navigation_menu(message: Message, state: FSMContext):
    """Обробляє вибір опцій в навігаційному меню."""
    try:
        text = message.text
        logger.info(f"Користувач {message.from_user.id} вибрав опцію: {text}")

        # Маппінг опцій меню до станів
        menu_options = {
            "🥷 Персонажі": MenuStates.HEROES_MENU,
            "🏆 Турніри": MenuStates.TOURNAMENTS_MENU,
            "📚 Гайди": MenuStates.GUIDES_MENU,
            "🛡️ Білди": MenuStates.BUILDS_MENU,
            "🧑‍🤝‍🧑 Команди": MenuStates.TEAMS_MENU,
            "🧩 Челендж": MenuStates.CHALLENGES_MENU,
            "🚀 Буст": MenuStates.BUST_MENU,
            "💰 Торгівля": MenuStates.TRADING_MENU,
            "🔙 Назад": MenuStates.MAIN_MENU
        }

        if text in menu_options:
            await state.set_state(menu_options[text])
            await message.answer(f"Ви перейшли до розділу {text}")
        else:
            await message.answer("Невідома опція. Будь ласка, виберіть опцію з меню.")

    except Exception as e:
        logger.error(f"Помилка при обробці вибору в навігаційному меню: {e}")
        await handle_navigation_error(message.bot, message.chat.id, state)

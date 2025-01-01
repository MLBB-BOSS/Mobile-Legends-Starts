from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from logging import getLogger
from typing import Optional

from utils.message_utils import MessageManager
from states.menu_states import IntroState, MainMenuState  # Змінено імпорт
from keyboards.menus import Keyboards
from texts import Messages

# ... решта коду залишається без змін

class IntroHandler:
    """Обробник вступної частини бота"""

    def __init__(self, message_manager: Optional[MessageManager] = None):
        """
        Ініціалізація обробника вступу.
        
        Args:
            message_manager: Менеджер повідомлень для управління відправкою/редагуванням
        """
        self.router = Router(name="intro")
        self.message_manager = message_manager
        self.logger = getLogger(__name__)
        self.keyboards = Keyboards()  # Створюємо екземпляр клавіатур
        self._setup_router()

    def _setup_router(self) -> None:
        """Налаштування маршрутизатора"""
        self.router.message.register(self.start_intro, Command("start"))
        self.router.callback_query.register(
            self.handle_intro_navigation,
            F.data.startswith("intro_")
        )

    async def start_intro(self, message: types.Message, state: FSMContext) -> None:
        """
        Обробка команди /start та початок вступу.
        
        Args:
            message: Повідомлення від користувача
            state: Стан FSM
        """
        try:
            self.logger.info(f"Starting intro for user {message.from_user.id}")
            
            await state.set_state(IntroState.page_1)
            
            if self.message_manager:
                await self.message_manager.send_or_edit(
                    chat_id=message.chat.id,
                    text=Messages.Intro.PAGE_1,
                    keyboard=self.keyboards.intro_keyboard(1)
                )
            else:
                await message.answer(
                    text=Messages.Intro.PAGE_1,
                    reply_markup=self.keyboards.intro_keyboard(1)
                )
                
        except Exception as e:
            self.logger.error(f"Error in start_intro: {e}")
            await message.answer(Messages.Intro.ERROR)

    async def handle_intro_navigation(
        self,
        callback: types.CallbackQuery,
        state: FSMContext
    ) -> None:
        """
        Обробка навігації по сторінках вступу.
        
        Args:
            callback: Callback-запит від користувача
            state: Стан FSM
        """
        try:
            current_state = await state.get_state()
            if not current_state:
                await callback.answer(Messages.Intro.STATE_ERROR)
                return
                
            action = callback.data.split("_")[1]
            page = None
            keyboard = None
            
            if action == "next":
                page, next_state, text = self._get_next_page_data(current_state)
            elif action == "prev":
                page, next_state, text = self._get_prev_page_data(current_state)
            elif action == "complete":
                next_state = MainMenuState.main
                text = Messages.MainMenu.WELCOME
                keyboard = self.keyboards.main_menu()
            else:
                await callback.answer(Messages.Intro.NAV_ERROR)
                return
            
            await state.set_state(next_state)
            
            # Створюємо клавіатуру, якщо вона ще не створена
            if not keyboard and page:
                keyboard = self.keyboards.intro_keyboard(page)
            
            # Оновлюємо повідомлення
            await self._update_message(callback, text, keyboard)
            await callback.answer()
            
        except Exception as e:
            self.logger.error(f"Error in navigation: {e}")
            await callback.answer(Messages.Intro.ERROR)

    def _get_next_page_data(self, current_state: str) -> tuple:
        """Отримати дані для наступної сторінки"""
        if current_state == "IntroState:page_1":
            return 2, IntroState.page_2, Messages.Intro.PAGE_2
        elif current_state == "IntroState:page_2":
            return 3, IntroState.page_3, Messages.Intro.PAGE_3
        raise ValueError("Invalid state for next page")

    def _get_prev_page_data(self, current_state: str) -> tuple:
        """Отримати дані для попередньої сторінки"""
        if current_state == "IntroState:page_2":
            return 1, IntroState.page_1, Messages.Intro.PAGE_1
        elif current_state == "IntroState:page_3":
            return 2, IntroState.page_2, Messages.Intro.PAGE_2
        raise ValueError("Invalid state for previous page")

    async def _update_message(
        self,
        callback: types.CallbackQuery,
        text: str,
        keyboard: types.InlineKeyboardMarkup
    ) -> None:
        """Оновити повідомлення"""
        if self.message_manager:
            await self.message_manager.send_or_edit(
                chat_id=callback.message.chat.id,
                text=text,
                message_id=callback.message.message_id,
                keyboard=keyboard
            )
        else:
            await callback.message.edit_text(
                text=text,
                reply_markup=keyboard
            )

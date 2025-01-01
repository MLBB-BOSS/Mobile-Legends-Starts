# handlers/main_menu.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from states.menu_states import MainMenuState, NavigationState, ProfileState
from keyboards.main_menu import get_main_menu_keyboard, get_main_menu_inline_keyboard
from constants.menu_texts import MAIN_MENU_TEXT, MAIN_MENU_SCREEN_TEXT
from utils.interface_manager import UIState, update_interface, safe_delete_message
from .base_handler import BaseHandler

from aiogram.types import Message, CallbackQuery
from keyboards.main_menu import (
    get_main_menu_keyboard,
    get_main_menu_inline_keyboard,
    MainMenuCallbacks,
    MainMenuButtons
)

class MainMenuHandler(BaseHandler):
    def __init__(self):
        super().__init__(name="main_menu")
        self.register_handlers()

    def register_handlers(self):
        """Реєстрація обробників головного меню"""
        self.router.message.register(self.cmd_start, CommandStart())
        self.router.message.register(
            self.handle_main_menu, 
            MainMenuState.main
        )

    async def cmd_start(self, message: Message, state: FSMContext):
        """Обробка команди /start"""
        # Видаляємо повідомлення користувача
        await safe_delete_message(message.bot, message.chat.id, message.message_id)

        # Створюємо новий інтерактивний екран
        screen = await message.bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_SCREEN_TEXT,
            reply_markup=get_main_menu_inline_keyboard()
        )

        # Відправляємо пульт керування
        control = await message.bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_TEXT,
            reply_markup=get_main_menu_keyboard()
        )

        # Зберігаємо стан
        await state.set_state(MainMenuState.main)
        await state.update_data(
            bot_message_id=control.message_id,
            interactive_message_id=screen.message_id,
            last_text=MAIN_MENU_TEXT,
            last_keyboard=get_main_menu_keyboard()
        )

    async def handle_main_menu(self, message: Message, state: FSMContext):
        """Обробка кнопок головного меню"""
        match message.text:
            case "🧭 Навігація":
                await self.handle_transition(
                    message=message,
                    state=state,
                    bot=message.bot,
                    new_state=NavigationState.main,
                    control_text="Навігаційне меню\nОберіть розділ:",
                    control_markup=get_navigation_menu_keyboard(),
                    screen_text="🧭 Навігація по грі\n\nТут ви знайдете:\n- Інформацію про героїв\n- Білди та гайди\n- Турніри та команди",
                    screen_markup=get_navigation_inline_keyboard()
                )
                
            case "🪪 Мій Профіль":
                await self.handle_transition(
                    message=message,
                    state=state,
                    bot=message.bot,
                    new_state=ProfileState.main,
                    control_text="Меню профілю\nОберіть опцію:",
                    control_markup=get_profile_menu_keyboard(),
                    screen_text="👤 Ваш профіль\n\nТут ви можете:\n- Переглянути статистику\n- Керувати налаштуваннями\n- Перевірити досягнення",
                    screen_markup=get_profile_inline_keyboard()
                )

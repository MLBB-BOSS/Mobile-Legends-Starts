from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from keyboards.main_menu import get_main_menu_keyboard
from states.menu_states import MainMenuState, NavigationState, ProfileState
from constants.menu_texts import MAIN_MENU_TEXT, MAIN_MENU_SCREEN_TEXT
from utils.interface_manager import update_interface, safe_delete_message
from .base_handler import BaseHandler

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Визначення клавіатури для головного меню
def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Створює клавіатуру головного меню.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Почати", callback_data="start")],
            [InlineKeyboardButton(text="Налаштування", callback_data="settings")],
            [InlineKeyboardButton(text="Допомога", callback_data="help")]
        ]
    )

class MainMenuHandler(BaseHandler):
    def __init__(self):
        super().__init__(name="main_menu")
        self.register_handlers()

    def register_handlers(self):
        """Реєстрація обробників головного меню"""
        self.router.message.register(self.cmd_start, CommandStart())
        # Створюємо новий інтерактивний екран
        screen = await message.bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_SCREEN_TEXT,
            reply_markup=get_main_menu_keyboard()
        )

        # Зберігаємо стан
        await state.set_state(MainMenuState.main)
        await state.update_data(
            bot_message_id=screen.message_id,
            last_text=MAIN_MENU_TEXT,
            last_keyboard=get_main_menu_keyboard()
        )

    async def handle_main_menu(self, message: Message, state: FSMContext):
        """Обробка кнопок головного меню"""
        match message.text:
            case "🧭 Навігація":
                # Логіка переходу до навігації
                pass
            case "🪪 Мій Профіль":
                # Логіка переходу до профілю
                pass


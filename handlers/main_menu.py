from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from states.menu_states import MainMenuState
from constants.menu_texts import MAIN_MENU_TEXT, MAIN_MENU_SCREEN_TEXT
from utils.interface_manager import update_interface, safe_delete_message
from .base_handler import BaseHandler


# Визначення клавіатури для головного меню
def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Створює клавіатуру головного меню.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🧭 Навігація", callback_data="navigation")],
            [InlineKeyboardButton(text="🪪 Мій Профіль", callback_data="profile")],
            [InlineKeyboardButton(text="⚙️ Налаштування", callback_data="settings")],
            [InlineKeyboardButton(text="❓ Допомога", callback_data="help")]
        ]
    )


class MainMenuHandler(BaseHandler):
    def __init__(self):
        super().__init__(name="main_menu")
        self.register_handlers()

    def register_handlers(self):
        """Реєстрація обробників головного меню"""
        self.router.message.register(self.cmd_start, CommandStart())
        self.router.message.register(self.handle_main_menu, MainMenuState.main)

    async def cmd_start(self, message: Message, state: FSMContext):
        """
        Обробка команди /start.
        """
        # Видаляємо повідомлення користувача
        await safe_delete_message(message.bot, message.chat.id, message.message_id)

        # Відправляємо екран головного меню
        screen = await message.bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_SCREEN_TEXT,
            reply_markup=get_main_menu_keyboard()
        )

        # Зберігаємо стан і дані для головного меню
        await state.set_state(MainMenuState.main)
        await state.update_data(
            bot_message_id=screen.message_id,
            last_text=MAIN_MENU_TEXT,
            last_keyboard=get_main_menu_keyboard()
        )

    async def handle_main_menu(self, message: Message, state: FSMContext):
        """
        Обробка кнопок головного меню.
        """
        # Отримуємо callback_data з повідомлення
        user_input = message.text

        # Логіка обробки кнопок
        match user_input:
            case "🧭 Навігація":
                await message.answer("🔍 Переходжу до навігації...")
                # Логіка переходу до навігації (перевести в NavigationState)
                await state.set_state(MainMenuState.settings)

            case "🪪 Мій Профіль":
                await message.answer("👤 Відображаю профіль...")
                # Логіка переходу до профілю (перевести в ProfileState)
                await state.set_state(MainMenuState.profile)

            case "⚙️ Налаштування":
                await message.answer("⚙️ Перехід до налаштувань...")
                # Логіка переходу до налаштувань
                await state.set_state(MainMenuState.settings)

            case "❓ Допомога":
                await message.answer("📘 Ось інструкція по використанню бота.")
                # Логіка відображення допомоги

            case _:
                await message.answer("❌ Невідома команда. Спробуйте ще раз.")

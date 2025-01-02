from aiogram import Router
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from states.menu_states import MainMenuState
from utils.interface_manager import safe_delete_message
from constants.menu_texts import MAIN_MENU_TEXT, MAIN_MENU_SCREEN_TEXT

# Визначення клавіатури для головного меню
def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    """
    Створює клавіатуру головного меню.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Профіль", callback_data="profile")],
            [InlineKeyboardButton(text="Налаштування", callback_data="settings")],
            [InlineKeyboardButton(text="Турніри", callback_data="tournaments")],
            [InlineKeyboardButton(text="Скріншоти", callback_data="screenshots")],
            [InlineKeyboardButton(text="Допомога", callback_data="help")]
        ]
    )

class MainMenuHandler:
    def __init__(self):
        """Ініціалізація маршрутизатора для головного меню"""
        self.router = Router()
        self.register_handlers()

    def register_handlers(self):
        """Реєстрація обробників головного меню"""
        self.router.message.register(self.cmd_start, CommandStart())
        self.router.message.register(self.handle_main_menu, MainMenuState.main)

    async def cmd_start(self, message: Message, state: FSMContext):
        """Обробка команди /start"""
        # Видаляємо повідомлення користувача
        await safe_delete_message(message.bot, message.chat.id, message.message_id)

        # Логування отриманої команди
        print(f"Received /start from user: {message.from_user.id}")

        # Створюємо новий інтерактивний екран
        screen = await message.bot.send_message(
            chat_id=message.chat.id,
            text=MAIN_MENU_SCREEN_TEXT,
            reply_markup=get_main_menu_keyboard()
        )

        # Логування створення екрану
        print(f"Main menu screen sent to user: {message.from_user.id}")

        # Зберігаємо стан
        await state.set_state(MainMenuState.main)
        await state.update_data(
            bot_message_id=screen.message_id,
            last_text=MAIN_MENU_TEXT,
            last_keyboard=get_main_menu_keyboard()
        )

    async def handle_main_menu(self, message: Message, state: FSMContext):
        """Обробка повідомлень у стані головного меню"""
        match message.text:
            case "Профіль":
                await message.answer("🪪 Відкриваємо ваш профіль...")
            case "Налаштування":
                await message.answer("⚙️ Переходимо до налаштувань...")
            case "Турніри":
                await message.answer("🏆 Перегляд турнірів...")
            case "Скріншоти":
                await message.answer("📸 Список скріншотів...")
            case "Допомога":
                await message.answer("🆘 Інформація про допомогу...")
            case _:
                await message.answer("⚠️ Невідома команда. Будь ласка, скористайтеся меню.")

# Створення інстансу MainMenuHandler
main_menu_handler = MainMenuHandler()
# Експорт маршрутизатора
router = main_menu_handler.router

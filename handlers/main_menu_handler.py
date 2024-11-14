# handlers/main_menu_handler.py
from aiogram import types, Router
from aiogram.filters import Command
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

router = Router()

@router.message(Command("start"))
async def main_menu(message: types.Message):
    # Створюємо клавіатуру головного меню
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("🧙‍♂️ Персонажі"), KeyboardButton("📚 Гайди")],
            [KeyboardButton("🏆 Турніри"), KeyboardButton("🔄 Оновлення")],
            [KeyboardButton("🆓 Початківець"), KeyboardButton("🔍 Пошук")],
            [KeyboardButton("📰 Новини"), KeyboardButton("💡 Допомога")],
            [KeyboardButton("🎮 Вікторини"), KeyboardButton("📝 Реєстрація")]
        ],
        resize_keyboard=True  # Робимо кнопки меншими для зручності
    )

    # Відправляємо повідомлення з головним меню
    await message.answer("Оберіть одну з опцій нижче:", reply_markup=keyboard)

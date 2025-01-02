# handlers/start.py

from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import logging

logger = logging.getLogger(__name__)

async def cmd_start(message: types.Message):
    """
    Обробник команди /start.
    Відправляє повідомлення з інтерактивними кнопками.
    """
    keyboard = InlineKeyboardMarkup(row_width=2)
    buttons = [
        InlineKeyboardButton(text="🧭 Навігація", callback_data="navigate"),
        InlineKeyboardButton(text="🪪 Мій Профіль", callback_data="profile"),
    ]
    keyboard.add(*buttons)

    await message.answer("Вітаю! Оберіть одну з опцій нижче:", reply_markup=keyboard)

def register_start_handler(dp: Dispatcher):
    """
    Реєструє хендлер для команди /start.
    """
    dp.message.register(cmd_start, commands="start", state="*")

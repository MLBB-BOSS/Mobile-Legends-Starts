# handlers/start.py

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
import logging

# Create a router instance
router = Router()

logger = logging.getLogger(__name__)

@router.message(Command("start"))
async def cmd_start(message: Message):
    """
    Обробник команди /start.
    Відправляє повідомлення з інтерактивними кнопками.
    """
    # Create buttons first
    buttons = [
        [
            InlineKeyboardButton(text="🧭 Навігація", callback_data="navigate"),
            InlineKeyboardButton(text="🪪 Мій Профіль", callback_data="profile")
        ]
    ]
    
    # Create keyboard with the buttons
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)

    await message.answer("Вітаю! Оберіть одну з опцій нижче:", reply_markup=keyboard)

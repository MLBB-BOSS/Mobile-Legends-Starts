# handlers/main_menu.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.main_menu import get_main_keyboard
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Вітаємо! Виберіть опцію:", reply_markup=get_main_keyboard())

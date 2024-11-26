# handlers/characters.py
from aiogram import Router, F
from aiogram.types import Message
from keyboards.characters_menu import get_characters_keyboard
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(F.text == "🥷 Персонажі")
async def show_characters_menu(message: Message):
    await message.answer("Оберіть тип героя:", reply_markup=get_characters_keyboard())

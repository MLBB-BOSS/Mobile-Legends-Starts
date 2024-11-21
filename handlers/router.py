# handlers/router.py - маршрутизація для команд /start і /menu

from aiogram import Router
from aiogram.types import Message
from keyboards.main_menu import MainMenuKeyboard
from utils.localization import Localization

router = Router()

@router.message(commands=["start", "menu"])
async def send_main_menu(message: Message):
    lang = "uk"
    loc = Localization(lang)
    await message.answer(
        text=loc.get_message("messages.main_menu"),
        reply_markup=MainMenuKeyboard.get_keyboard(lang=lang)
    )

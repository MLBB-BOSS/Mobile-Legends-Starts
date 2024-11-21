# File: handlers/profile_handlers.py
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Text
from keyboards.profile_menu import ProfileMenu

router = Router()

@router.message(Text("Профіль"))
async def handle_profile(message: Message):
    await message.answer(
        "Це ваш профіль. Оберіть дію:",
        reply_markup=ProfileMenu.get_profile_menu()
    )

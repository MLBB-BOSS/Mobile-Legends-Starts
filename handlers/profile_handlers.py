# handlers/profile_handlers.py
from aiogram import Router, F
from aiogram.types import Message
from keyboards.profile_menu import ProfileMenu

router = Router()

@router.message(F.text == "🪪 Мій профіль")
async def handle_my_profile(message: Message):
    await message.reply(
        "Це меню вашого профілю. Оберіть опцію:",
        reply_markup=ProfileMenu.get_profile_menu()
    )

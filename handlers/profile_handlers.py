from aiogram import Router, F
from aiogram.types import Message
from keyboards.profile_menu import ProfileMenu
from keyboards.main_menu import MainMenu

router = Router()

@router.message(F.text == "🪪 Профіль")
async def handle_profile(message: Message):
    await message.reply(
        "Це розділ профілю. Оберіть опцію:",
        reply_markup=ProfileMenu.get_profile_menu()
    )

@router.message(F.text == "🔙 Назад")
async def handle_back(message: Message):
    await message.reply(
        "Повернення до головного меню. Оберіть дію:",
        reply_markup=MainMenu.get_main_menu()
    )

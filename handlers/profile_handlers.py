from aiogram import Router, F
from aiogram.types import Message
from keyboards.profile_menu import ProfileMenu
from keyboards.main_menu import MainMenu

router = Router()

@router.message(F.text == "🪪 Профіль")
async def handle_profile(message: Message):
    """Обробка кнопки 'Профіль'."""
    await message.reply(
        "Це розділ профілю. Оберіть опцію:",
        reply_markup=ProfileMenu.get_profile_menu()
    )

@router.message(F.text == "🔙 Назад")
async def handle_back_to_main_menu_from_profile(message: Message):
    """Обробка кнопки 'Назад' для повернення до головного меню з профілю."""
    await message.reply(
        "Повернення до головного меню. Оберіть дію:",
        reply_markup=MainMenu.get_main_menu()
    )

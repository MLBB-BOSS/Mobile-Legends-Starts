from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.main_menu import MainMenu

router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    """Обробка команди /start"""
    user_name = message.from_user.first_name
    await message.reply(
        f"Ласкаво просимо до бота, {user_name}! Оберіть дію:",
        reply_markup=MainMenu.get_main_menu()
    )

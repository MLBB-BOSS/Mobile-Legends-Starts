from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.main_menu import MainMenu

router = Router()

@router.message(Command("start"))
async def start_command(message: Message):
    await message.answer(
        "Ласкаво просимо до бота! Оберіть дію:",
        reply_markup=MainMenu.get_main_menu()
    )

from aiogram import Router, F
from aiogram.types import Message
from keyboards.start_command import StartMenu

router = Router()

@router.message(F.text == "/start")
async def handle_start_command(message: Message):
    keyboard = StartMenu.get_start_menu()
    await message.answer("Вітаю! Це стартове меню вашого бота.", reply_markup=keyboard)

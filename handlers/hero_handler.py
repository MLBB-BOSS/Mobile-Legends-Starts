from aiogram import Router, F
from aiogram.filters import Command, Text
from aiogram.types import Message
from aiogram.utils.markdown import hbold

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        f"Привіт, {hbold(message.from_user.full_name)}!\n"
        "Я бот для Mobile Legends. Чим можу допомогти?"
    )

@router.message(Text(text="герої", ignore_case=True))
async def show_heroes(message: Message):
    await message.answer("Ось список доступних героїв:")
    # Тут можна додати логіку для відображення героїв

@router.message(Command("help"))
async def cmd_help(message: Message):
    help_text = (
        "Доступні команди:\n"
        "/start - Почати роботу з ботом\n"
        "/help - Показати це повідомлення\n"
        "Напишіть 'герої' щоб побачити список героїв"
    )
    await message.answer(help_text)

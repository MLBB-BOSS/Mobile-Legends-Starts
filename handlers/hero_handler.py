from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        f"Привіт, {hbold(message.from_user.full_name)}!\n"
        "Я бот для Mobile Legends. Чим можу допомогти?"
    )

@router.message(F.text.lower() == "герої")
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

# Обробка різних варіантів тексту
@router.message(F.text.lower().in_(["герої", "heroes", "персонажі"]))
async def show_heroes_alternative(message: Message):
    await message.answer("Ось список доступних героїв:")
    # Логіка для відображення героїв

from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.menus import (
    get_main_menu,
    get_navigation_menu,
    get_heroes_menu,
    MenuButton
)

router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    """Обробник для команди /start"""
    await message.answer(
        "Привіт! Ласкаво просимо до бота. Оберіть опцію:",
        reply_markup=get_main_menu()
    )

@router.message(Command("help"))
async def cmd_help(message: Message):
    """Обробник для команди /help"""
    await message.answer(
        "Це довідка. Сюди можна додати інформацію про використання бота."
    )

@router.message(F.text == MenuButton.NAVIGATION.value)
async def navigation_menu(message: Message):
    """Обробник для кнопки Навігація"""
    await message.answer(
        "🧭 Навігація: Оберіть розділ:",
        reply_markup=get_navigation_menu()
    )

@router.message(F.text == MenuButton.HEROES.value)
async def heroes_menu(message: Message):
    """Обробник для кнопки Персонажі"""
    await message.answer(
        "🛡️ Персонажі: Оберіть клас персонажів:",
        reply_markup=get_heroes_menu()
    )

@router.message(F.text == MenuButton.BACK.value)
async def back_handler(message: Message):
    """Обробник для кнопки Назад"""
    await message.answer(
        "Ви повернулися до головного меню.",
        reply_markup=get_main_menu()
    )

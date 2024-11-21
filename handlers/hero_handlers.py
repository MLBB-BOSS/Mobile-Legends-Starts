# handlers/hero_handlers.py
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.navigation_keyboard import NavigationKeyboard
from keyboards.keyboard_buttons import Buttons

router = Router()
kb = NavigationKeyboard()

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer(
        "Вітаю! Я MLBB-BOSS бот. Оберіть опцію:",
        reply_markup=kb.get_navigation_menu()
    )

@router.message(F.text == Buttons.NAVIGATION)
async def navigation_menu(message: Message):
    await message.answer(
        "Оберіть розділ навігації:",
        reply_markup=kb.get_navigation_menu()
    )

@router.message(F.text == Buttons.CHARACTERS)
async def characters_menu(message: Message):
    await message.answer(
        "Оберіть персонажа:",
        reply_markup=kb.get_characters_menu()
    )

@router.message(F.text == Buttons.BACK_TO_MAIN)
async def back_to_main(message: Message):
    await message.answer(
        "Головне меню:",
        reply_markup=kb.get_navigation_menu()
    )

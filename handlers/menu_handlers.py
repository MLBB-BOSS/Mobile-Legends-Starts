from aiogram import Router, F
from aiogram.types import Message
from keyboards import MenuKeyboard, Buttons
import logging

logger = logging.getLogger(__name__)
router = Router()
kb = MenuKeyboard()

@router.message(F.text == Buttons.NAVIGATION.value)
async def show_navigation(message: Message):
    await message.answer(
        "Меню навігації:",
        reply_markup=kb.get_navigation_menu()
    )

@router.message(F.text == Buttons.HEROES.value)
async def show_heroes(message: Message):
    await message.answer(
        "Оберіть клас героя:",
        reply_markup=kb.get_heroes_menu()
    )

@router.message(F.text == Buttons.PROFILE.value)
async def show_profile(message: Message):
    await message.answer(
        "Ваш профіль:",
        reply_markup=kb.get_profile_menu()
    )

@router.message(F.text == Buttons.SETTINGS.value)
async def show_settings(message: Message):
    await message.answer(
        "Налаштування:",
        reply_markup=kb.get_settings_menu()
    )

@router.message(F.text == Buttons.MAIN_MENU.value)
async def show_main_menu(message: Message):
    await message.answer(
        "Головне меню:",
        reply_markup=kb.get_main_menu()
    )

@router.message(F.text == Buttons.BACK.value)
async def handle_back(message: Message):
    await message.answer(
        "Повертаємося назад:",
        reply_markup=kb.get_main_menu()
    )

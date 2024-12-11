# handlers/callbacks.py

from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline_menus import CallbackData, get_main_inline_keyboard, get_heroes_inline_keyboard
from utils.menu_messages import MenuMessages
from utils.message_formatter import MessageFormatter

router = Router()

@router.callback_query(F.data == CallbackData.HEROES.value)
async def process_heroes_menu(callback: CallbackQuery):
    """Обробка натискання кнопки Персонажі"""
    menu_text = MenuMessages.get_heroes_menu_text()
    await MessageFormatter.update_menu_message(
        message=callback.message,
        title=menu_text["title"],
        description=menu_text["description"],
        keyboard=get_heroes_inline_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == CallbackData.GUIDES.value)
async def process_guides_menu(callback: CallbackQuery):
    """Обробка натискання кнопки Гайди"""
    menu_text = MenuMessages.get_guides_menu_text()
    await MessageFormatter.update_menu_message(
        message=callback.message,
        title=menu_text["title"],
        description=menu_text["description"],
        keyboard=get_guides_inline_keyboard()  # Створіть цю функцію
    )
    await callback.answer()

@router.callback_query(F.data == CallbackData.BACK.value)
async def process_back_button(callback: CallbackQuery):
    """Обробка натискання кнопки Назад"""
    main_menu_text = {
        "title": "🎮 Головне меню",
        "description": "Оберіть розділ для навігації:"
    }
    await MessageFormatter.update_menu_message(
        message=callback.message,
        title=main_menu_text["title"],
        description=main_menu_text["description"],
        keyboard=get_main_inline_keyboard()
    )
    await callback.answer()

# Додайте інші обробники

# handlers/callbacks.py

import logging
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.enums import ParseMode

# Приклад: якщо у вас є якийсь Enum або датаклас CallbackData
# з файла keyboards/inline_menus або подібного
from keyboards.inline_menus import (
    CallbackData,
    get_main_inline_keyboard,
    get_heroes_inline_keyboard,
    get_guides_inline_keyboard
)
from utils.menu_messages import MenuMessages
from utils.message_formatter import MessageFormatter

logger = logging.getLogger(__name__)
router = Router()

@router.callback_query(F.data == CallbackData.HEROES.value)
async def process_heroes_menu(callback: CallbackQuery):
    """
    Обробка інлайн-кнопки, яка відкриває меню «Герої».
    Це приклад використання інлайн-клавіатури, коли ви хочете
    відобразити якесь додаткове вікно/повідомлення/список героїв.
    """
    logger.info(f"Користувач натиснув інлайн-кнопку HEROES зі значенням: {CallbackData.HEROES.value}")

    # Тут можемо отримати будь-які тексти з утиліт чи хелперів
    menu_text = MenuMessages.get_heroes_menu_text()

    # Припустимо, MessageFormatter — це ваш кастомний клас для оновлення повідомлень
    await MessageFormatter.update_menu_message(
        message=callback.message,
        title=menu_text["title"],
        description=menu_text["description"],
        keyboard=get_heroes_inline_keyboard()  # Повертає інлайн-кнопки
    )
    await callback.answer()

@router.callback_query(F.data == CallbackData.GUIDES.value)
async def process_guides_menu(callback: CallbackQuery):
    """
    Обробка інлайн-кнопки, яка відкриває меню «Гайди».
    """
    logger.info(f"Користувач натиснув інлайн-кнопку GUIDES зі значенням: {CallbackData.GUIDES.value}")

    menu_text = MenuMessages.get_guides_menu_text()

    await MessageFormatter.update_menu_message(
        message=callback.message,
        title=menu_text["title"],
        description=menu_text["description"],
        keyboard=get_guides_inline_keyboard()  # Повертає інлайн-кнопки
    )
    await callback.answer()

@router.callback_query(F.data == CallbackData.BACK.value)
async def process_back_button(callback: CallbackQuery):
    """
    Обробка натискання інлайн-кнопки «Назад» (Back).
    Повертаємося до головного інлайн-меню чи іншого стану.
    """
    logger.info(f"Користувач натиснув інлайн-кнопку BACK зі значенням: {CallbackData.BACK.value}")

    main_menu_text = {
        "title": "🎮 Головне меню",
        "description": "Оберіть розділ для навігації:"
    }

    # Припустимо, main-inline-клавіатура у нас будується через get_main_inline_keyboard()
    # Якщо потрібно, можна вставити будь-яку іншу логіку
    await MessageFormatter.update_menu_message(
        message=callback.message,
        title=main_menu_text["title"],
        description=main_menu_text["description"],
        keyboard=get_main_inline_keyboard()
    )

    # Відправляємо callback.answer(), аби прибрати «годинник» у Telegram
    await callback.answer()
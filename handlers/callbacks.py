# handlers/callbacks.py

from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline_menus import CallbackData, get_main_inline_keyboard, get_heroes_inline_keyboard, get_guides_inline_keyboard
from utils.menu_messages import MenuMessages
from utils.message_formatter import MessageFormatter
import logging

router = Router()

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.callback_query(F.data == CallbackData.HEROES.value)
async def process_heroes_menu(callback: CallbackQuery):
    """Обробка натискання кнопки Персонажі"""
    user_id = callback.from_user.id
    logger.info(f"User {user_id} pressed heroes")
    
    menu_text = MenuMessages.get_heroes_menu_text()
    try:
        await MessageFormatter.update_menu_message(
            message=callback.message,
            title=menu_text["title"],
            description=menu_text["description"],
            keyboard=get_heroes_inline_keyboard()
        )
        logger.info(f"Heroes menu updated for user {user_id}")
    except Exception as e:
        logger.error(f"Failed to update heroes menu for user {user_id}: {e}")
        await callback.message.answer("Сталася помилка при оновленні меню. Спробуйте пізніше.")
    
    await callback.answer()

@router.callback_query(F.data == CallbackData.GUIDES.value)
async def process_guides_menu(callback: CallbackQuery):
    """Обробка натискання кнопки Гайди"""
    user_id = callback.from_user.id
    logger.info(f"User {user_id} pressed guides")
    
    menu_text = MenuMessages.get_guides_menu_text()
    try:
        await MessageFormatter.update_menu_message(
            message=callback.message,
            title=menu_text["title"],
            description=menu_text["description"],
            keyboard=get_guides_inline_keyboard()
        )
        logger.info(f"Guides menu updated for user {user_id}")
    except Exception as e:
        logger.error(f"Failed to update guides menu for user {user_id}: {e}")
        await callback.message.answer("Сталася помилка при оновленні меню. Спробуйте пізніше.")
    
    await callback.answer()

@router.callback_query(F.data == CallbackData.BACK.value)
async def process_back_button(callback: CallbackQuery):
    """Обробка натискання кнопки Назад"""
    user_id = callback.from_user.id
    logger.info(f"User {user_id} pressed back")
    
    main_menu_text = {
        "title": "🎮 Головне меню",
        "description": "Оберіть розділ для навігації:"
    }
    try:
        await MessageFormatter.update_menu_message(
            message=callback.message,
            title=main_menu_text["title"],
            description=main_menu_text["description"],
            keyboard=get_main_inline_keyboard()
        )
        logger.info(f"Returned to main menu for user {user_id}")
    except Exception as e:
        logger.error(f"Failed to return to main menu for user {user_id}: {e}")
        await callback.message.answer("Сталася помилка при поверненні до головного меню. Спробуйте пізніше.")
    
    await callback.answer()

# Додайте інші обробники за потребою

@router.callback_query()
async def handle_unknown_callback(callback: CallbackQuery):
    """Обробка невідомих callback'ів"""
    user_id = callback.from_user.id
    data = callback.data
    logger.warning(f"User {user_id} pressed unknown callback: {data}")
    
    try:
        await callback.answer("Невідома команда. Будь ласка, використовуйте надані кнопки для навігації.")
    except Exception as e:
        logger.error(f"Failed to send unknown command response to user {user_id}: {e}")

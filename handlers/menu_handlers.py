# Шлях: handlers/menu_handlers.py
# Цей файл містить всі обробники для меню
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from typing import Optional
import logging

# Імпортуємо наші клавіатури
from keyboards.main_menu import MainMenu

# Налаштовуємо логування
logger = logging.getLogger(__name__)

# Створюємо роутер для меню
router = Router(name="menu_router")

# Створюємо клас для станів меню
class MenuStates(StatesGroup):
    main = State()
    heroes = State()
    builds = State()
    guides = State()
    statistics = State()
    profile = State()
    settings = State()

# Обробник команди /menu
@router.message(Command("menu"))
@router.message(F.text == "🏠 Головне меню")
async def show_main_menu(message: Message, state: FSMContext):
    """Показує головне меню"""
    try:
        # Створюємо екземпляр головного меню
        menu = MainMenu()
        # Отримуємо клавіатуру та текст
        keyboard = await menu.get_keyboard()
        text = await menu.get_text()
        # Встановлюємо стан головного меню
        await state.set_state(MenuStates.main)
        # Відправляємо повідомлення з меню
        await message.answer(text, reply_markup=keyboard)
        logger.info(f"Показано головне меню користувачу {message.from_user.id}")
    except Exception as e:
        logger.error(f"Помилка при показі головного меню: {e}")
        await message.answer("Виникла помилка. Спробуйте пізніше.")

# Обробник натискань на кнопки меню
@router.callback_query(F.data.startswith("menu_"))
async def handle_menu_navigation(callback: CallbackQuery, state: FSMContext):
    """Обробляє навігацію по меню"""
    try:
        # Отримуємо назву розділу меню з callback_data
        section = callback.data.split('_')[1]
        await callback.answer(f"Розділ {section} в розробці!")
        
        logger.info(f"Користувач {callback.from_user.id} намагався перейти до розділу {section}")
    except Exception as e:
        logger.error(f"Помилка при навігації по меню: {e}")
        await callback.answer("Виникла помилка. Спробуйте пізніше.", show_alert=True)

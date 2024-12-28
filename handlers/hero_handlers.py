from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from typing import Dict, List, Optional
import logging
from states import MenuStates
from database.hero_database import HeroDatabase

# Створюємо роутер
router = Router()

# Налаштування логування
logger = logging.getLogger(__name__)

# Константи для меню героїв
HERO_ROLES = {
    "TANK": "Танк",
    "FIGHTER": "Файтер",
    "ASSASSIN": "Асасин",
    "MAGE": "Маг",
    "MARKSMAN": "Стрілець",
    "SUPPORT": "Підтримка"
}

# Тексти повідомлень
TEXTS = {
    'select_role': "Виберіть роль героя:",
    'select_hero': "Виберіть героя:",
    'hero_not_found': "Герой не знайдений. Виберіть героя зі списку",
    'enter_hero_name': "Введіть ім'я героя для пошуку:",
    'no_heroes_found': "Героїв не знайдено. Спробуйте інший запит",
    'error': "Виникла помилка. Спробуйте пізніше або поверніться до головного меню",
    'main_menu': "Головне меню"
}

@router.message(F.state == MenuStates.HEROES_MENU)
async def handle_hero_selection(message: Message, state: FSMContext, bot: Bot):
    """
    Обробник вибору героя в меню героїв.
    """
    try:
        user_choice = message.text.strip()
        data = await state.get_data()
        current_submenu = data.get('heroes_submenu', 'main')

        if current_submenu == 'main':
            await handle_main_submenu(message, state, bot, user_choice)
        elif current_submenu == 'hero_list':
            await handle_hero_list_submenu(message, state, bot, user_choice, data)
        elif current_submenu == 'search':
            await handle_search_submenu(message, state, bot, user_choice)

    except Exception as e:
        logger.error(f"Error in hero selection menu: {str(e)}")
        await handle_error(message, bot)

async def handle_main_submenu(message: Message, state: FSMContext, bot: Bot, user_choice: str):
    """Обробка головного підменю героїв"""
    if user_choice in HERO_ROLES.values():
        role = [k for k, v in HERO_ROLES.items() if v == user_choice][0]
        heroes = await HeroDatabase.get_heroes_by_role(role)
        
        await state.update_data(
            heroes_submenu='hero_list',
            selected_role=role,
            heroes_list=heroes
        )
        
        await show_heroes_list(message, bot, heroes)
        
    elif user_choice.lower() == "пошук героя":
        await state.update_data(heroes_submenu='search')
        await message.answer(
            TEXTS['enter_hero_name'],
            reply_markup=get_hero_search_keyboard()
        )
        
    elif user_choice.lower() == "назад":
        await return_to_main_menu(message, state, bot)
        
    else:
        await message.answer(
            TEXTS['select_role'],
            reply_markup=get_heroes_main_keyboard()
        )

async def handle_hero_list_submenu(message: Message, state: FSMContext, bot: Bot, 
                                 user_choice: str, data: Dict):
    """Обробка підменю списку героїв"""
    heroes_list = data.get('heroes_list', [])
    selected_hero = next(
        (hero for hero in heroes_list if hero['name'] == user_choice),
        None
    )
    
    if selected_hero:
        await show_hero_details(message, bot, selected_hero)
        
    elif user_choice.lower() == "назад":
        await state.update_data(heroes_submenu='main')
        await message.answer(
            TEXTS['select_role'],
            reply_markup=get_heroes_main_keyboard()
        )
        
    else:
        await message.answer(
            TEXTS['hero_not_found'],
            reply_markup=get_hero_list_keyboard(heroes_list)
        )

async def handle_search_submenu(message: Message, state: FSMContext, bot: Bot, user_choice: str):
    """Обробка підменю пошуку героїв"""
    if user_choice.lower() == "назад":
        await state.update_data(heroes_submenu='main')
        await message.answer(
            TEXTS['select_role'],
            reply_markup=get_heroes_main_keyboard()
        )
    else:
        found_heroes = await HeroDatabase.search_heroes(user_choice)
        if found_heroes:
            await show_heroes_list(message, bot, found_heroes)
        else:
            await message.answer(
                TEXTS['no_heroes_found'],
                reply_markup=get_hero_search_keyboard()
            )

[... Решта функцій залишається такою ж, як у попередньому коді ...]

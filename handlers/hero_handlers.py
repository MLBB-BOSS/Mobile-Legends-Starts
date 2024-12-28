# hero_handlers.py

import logging
from typing import Dict, List, Optional

# Aiogram
from aiogram import F, Router, Bot
from aiogram.types import (
    Message, 
    CallbackQuery, 
    ReplyKeyboardRemove, 
    ReplyKeyboardMarkup, 
    KeyboardButton
)
from aiogram.fsm.context import FSMContext

# Ваші власні модулі
from states import MenuStates
from database.hero_database import HeroDatabase  # Приклад: ваш клас/модуль для взаємодії з БД
from utils.message_utils import safe_delete_message

# Ініціалізація логера та роутера
logger = logging.getLogger(__name__)
router = Router()

# Приклад текстових констант
TEXTS = {
    'select_role': "Виберіть роль героя:",
    'select_hero': "Виберіть героя:",
    'hero_not_found': "Герой не знайдений. Виберіть героя зі списку",
    'enter_hero_name': "Введіть ім'я героя для пошуку:",
    'no_heroes_found': "Героїв не знайдено. Спробуйте інший запит",
    'error': "Виникла помилка. Спробуйте пізніше або поверніться до головного меню",
    'main_menu': "Головне меню"
}

# Константи для меню героїв (ролі/класи)
HERO_ROLES = {
    "TANK": "Танк",
    "FIGHTER": "Файтер",
    "ASSASSIN": "Асасин",
    "MAGE": "Маг",
    "MARKSMAN": "Стрілець",
    "SUPPORT": "Підтримка"
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


# -------------------------------------------------------------------
# Підменю №1: Обробка "головного" підменю (ролі героїв, пошук, тощо)
# -------------------------------------------------------------------
async def handle_main_submenu(message: Message, state: FSMContext, bot: Bot, user_choice: str):
    """Обробка головного підменю героїв."""
    if user_choice in HERO_ROLES.values():
        # Користувач обрав конкретну роль (наприклад, "Танк")
        role = [k for k, v in HERO_ROLES.items() if v == user_choice][0]

        # Отримуємо список героїв з БД
        heroes = await HeroDatabase.get_heroes_by_role(role)

        await state.update_data(
            heroes_submenu='hero_list',
            selected_role=role,
            heroes_list=heroes
        )
        
        # Показуємо список героїв
        await show_heroes_list(message, bot, heroes)
        
    elif user_choice.lower() == "пошук героя":
        # Якщо користувач хоче пошукати героя
        await state.update_data(heroes_submenu='search')
        await message.answer(
            TEXTS['enter_hero_name'],
            reply_markup=get_hero_search_keyboard()  # Показуємо клавіатуру для пошуку
        )
        
    elif user_choice.lower() == "назад":
        # Якщо натиснув "назад" — повертаємося в головне меню
        await return_to_main_menu(message, state, bot)
        
    else:
        # Якщо не впізнали команду/роль — повторно показуємо ролі
        await message.answer(
            TEXTS['select_role'],
            reply_markup=get_heroes_main_keyboard()
        )


# -------------------------------------------------------------------
# Підменю №2: Обробка списку героїв, коли роль уже обрана
# -------------------------------------------------------------------
async def handle_hero_list_submenu(
    message: Message, 
    state: FSMContext, 
    bot: Bot, 
    user_choice: str, 
    data: Dict
):
    """Обробка підменю списку героїв."""
    heroes_list = data.get('heroes_list', [])
    selected_hero = next(
        (hero for hero in heroes_list if hero['name'] == user_choice),
        None
    )
    
    if selected_hero:
        await show_hero_details(message, bot, selected_hero)
        
    elif user_choice.lower() == "назад":
        # Повертаємося на рівень обрання ролі
        await state.update_data(heroes_submenu='main')
        await message.answer(
            TEXTS['select_role'],
            reply_markup=get_heroes_main_keyboard()
        )
        
    else:
        # Якщо такого героя у списку немає
        await message.answer(
            TEXTS['hero_not_found'],
            reply_markup=get_hero_list_keyboard(heroes_list)
        )


# -------------------------------------------------------------------
# Підменю №3: Пошук героїв за введеним користувачем рядком
# -------------------------------------------------------------------
async def handle_search_submenu(message: Message, state: FSMContext, bot: Bot, user_choice: str):
    """Обробка підменю пошуку героїв."""
    if user_choice.lower() == "назад":
        # Повертаємося в «головне» підменю героїв
        await state.update_data(heroes_submenu='main')
        await message.answer(
            TEXTS['select_role'],
            reply_markup=get_heroes_main_keyboard()
        )
    else:
        # Виконуємо пошук у БД
        found_heroes = await HeroDatabase.search_heroes(user_choice)
        if found_heroes:
            await show_heroes_list(message, bot, found_heroes)
        else:
            await message.answer(
                TEXTS['no_heroes_found'],
                reply_markup=get_hero_search_keyboard()
            )


# -------------------------------------------------------------------
# ДОПОМІЖНІ ФУНКЦІЇ ДЛЯ ВІДОБРАЖЕННЯ КЛАВІАТУР, СПИСКІВ, ДЕТАЛЕЙ, ТОЩО
# -------------------------------------------------------------------

def get_heroes_main_keyboard() -> ReplyKeyboardMarkup:
    """
    Повертає клавіатуру з кнопками ролей (Танк, Файтер тощо) 
    та кнопкою «Пошук героя» і «Назад».
    """
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    
    # Додаємо кнопки з ролями
    for role_name in HERO_ROLES.values():
        kb.add(KeyboardButton(role_name))
    
    # Додаємо "Пошук героя" 
    kb.add(KeyboardButton("Пошук героя"))

    # Додаємо "Назад"
    kb.add(KeyboardButton("Назад"))
    return kb


def get_hero_list_keyboard(heroes_list: List[Dict]) -> ReplyKeyboardMarkup:
    """
    Створюємо клавіатуру зі списком імен героїв + кнопка «Назад».
    """
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for hero in heroes_list:
        kb.add(KeyboardButton(hero['name']))  # Припустимо, hero — це словник зі ключем 'name'
    kb.add(KeyboardButton("Назад"))
    return kb


def get_hero_search_keyboard() -> ReplyKeyboardMarkup:
    """
    Повертає клавіатуру для пошуку героя (просто кнопка «Назад»).
    """
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("Назад"))
    return kb


async def show_heroes_list(message: Message, bot: Bot, heroes: List[Dict]):
    """
    Відправляємо користувачеві повідомлення зі списком героїв та клавіатурою.
    """
    if not heroes:
        await message.answer(TEXTS['no_heroes_found'])
        return
    
    # Можемо вивести назви героїв у тексті, а також додати клавіатуру
    hero_names = ", ".join(hero['name'] for hero in heroes)
    text = f"Доступні герої:\n{hero_names}\n\nОберіть героя зі списку:"
    
    await message.answer(
        text,
        reply_markup=get_hero_list_keyboard(heroes)
    )


async def show_hero_details(message: Message, bot: Bot, hero: Dict):
    """
    Відображаємо деталі обраного героя (наприклад, його назву, опис тощо).
    """
    hero_name = hero.get('name', 'Невідомий')
    hero_description = hero.get('description', 'Опис відсутній')
    
    details_text = (
        f"**{hero_name}**\n"
        f"{hero_description}\n\n"
        "Щоб повернутися до списку героїв, натисніть «Назад»."
    )
    await message.answer(
        details_text,
        parse_mode="Markdown",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[[KeyboardButton("Назад")]],
            resize_keyboard=True
        )
    )


# -------------------------------------------------------------------
# ФУНКЦІЇ ДЛЯ ПОВЕРНЕННЯ У ГОЛОВНЕ МЕНЮ ЧИ ОПРАЦЮВАННЯ ПОМИЛОК
# -------------------------------------------------------------------
async def return_to_main_menu(message: Message, state: FSMContext, bot: Bot):
    """
    Функція повернення до головного меню.
    """
    await state.set_state(MenuStates.MAIN_MENU)
    await message.answer(
        TEXTS['main_menu'],
        reply_markup=ReplyKeyboardRemove()  # або своя клавіатура головного меню
    )


async def handle_error(message: Message, bot: Bot):
    """
    Функція для централізованого опрацювання помилок.
    """
    try:
        await message.answer(TEXTS['error'])
    except Exception as e:
        logger.critical(f"Fatal error while sending error message: {e}")

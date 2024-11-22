# handlers/heroes_handlers.py
from aiogram.types import Message
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
import logging

router = Router()
logger = logging.getLogger(__name__)

class SearchHeroStates(StatesGroup):
    waiting_for_hero_name = State()

@router.message(F.text == "🔎 Пошук Героя")
async def handle_search_hero(message: Message, state: FSMContext):
    logger.info("Натиснуто кнопку '🔎 Пошук Героя'")
    await message.answer("Введіть ім'я героя для пошуку інформації:")
    await state.set_state(SearchHeroStates.waiting_for_hero_name)

@router.message(SearchHeroStates.waiting_for_hero_name, F.text)
async def process_hero_name(message: Message, state: FSMContext):
    hero_name = message.text.strip()
    logger.info(f"Користувач шукає героя: {hero_name}")
    
    # Тут ви можете додати логіку пошуку героя у вашій базі даних або API
    # Наприклад:
    # hero_info = search_hero_in_database(hero_name)
    # if hero_info:
    #     await message.answer(f"Інформація про героя {hero_name}:\n{hero_info}")
    # else:
    #     await message.answer(f"Герой {hero_name} не знайдений.")
    
    # Для прикладу, ми просто відправимо загальне повідомлення
    await message.answer(f"Інформація про героя {hero_name}:\n- Опис героя\n- Навички\n- Статистика")
    
    await state.clear()

@router.message(F.text == "🔄 Назад до Навігації")
async def handle_back_to_navigation_from_heroes(message: Message):
    logger.info("Натиснуто кнопку '🔄 Назад до Навігації' у героях")
    from keyboards.menus import NavigationMenu
    keyboard = NavigationMenu.get_navigation_menu()
    await message.answer("Повернення до навігації. Оберіть дію:", reply_markup=keyboard)

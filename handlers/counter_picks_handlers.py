# handlers/counter_picks_handlers.py
from aiogram.types import Message
from aiogram import Router, F
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "🔎 Пошук Контр-піку")
async def handle_search_counter_pick(message: Message):
    logger.info("Натиснуто кнопку '🔎 Пошук Контр-піку'")
    await message.answer("Знайдіть ідеальний контр-пік для ворожого героя.")

@router.message(F.text == "📝 Список Героїв")
async def handle_list_of_heroes(message: Message):
    logger.info("Натиснуто кнопку '📝 Список Героїв'")
    await message.answer("Виберіть героя для перегляду можливих контр-піків.")

@router.message(F.text == "🔄 Назад до Навігації")
async def handle_back_to_navigation_from_counter_picks(message: Message):
    logger.info("Натиснуто кнопку '🔄 Назад до Навігації' у контр-піках")
    from keyboards.menus import NavigationMenu
    keyboard = NavigationMenu.get_navigation_menu()
    await message.answer("Повернення до навігації. Оберіть дію:", reply_markup=keyboard)

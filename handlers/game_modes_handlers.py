# handlers/game_modes_handlers.py
from aiogram.types import Message
from aiogram import Router, F
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "🪩 Класичний")
async def handle_classic_mode(message: Message):
    logger.info("Натиснуто кнопку '🪩 Класичний'")
    await message.answer("Основи геймплею в класичному режимі.")

@router.message(F.text == "🎮 Рейтинг")
async def handle_ranking_mode(message: Message):
    logger.info("Натиснуто кнопку '🎮 Рейтинг'")
    await message.answer("Підготуйтеся до змагань у рейтинговому режимі.")

@router.message(F.text == "🎭 Події")
async def handle_event_modes(message: Message):
    logger.info("Натиснуто кнопку '🎭 Події'")
    await message.answer("Тимчасові режими або тематичні події.")

@router.message(F.text == "🔄 Назад до Навігації")
async def handle_back_to_navigation_from_game_modes(message: Message):
    logger.info("Натиснуто кнопку '🔄 Назад до Навігації' у режимах гри")
    from keyboards.menus import NavigationMenu
    keyboard = NavigationMenu.get_navigation_menu()
    await message.answer("Повернення до навігації. Оберіть дію:", reply_markup=keyboard)

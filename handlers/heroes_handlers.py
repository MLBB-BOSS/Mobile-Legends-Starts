# handlers/heroes_handlers.py
from aiogram.types import Message
from aiogram import Router, F
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "🛡️ Герої")
async def show_heroes_menu(message: Message):
    logger.info("Натиснуто кнопку '🛡️ Герої'")
    from keyboards.heroes_menu import HeroesMenu
    keyboard = HeroesMenu.get_heroes_menu()
    await message.answer("Оберіть героя або класифікацію:", reply_markup=keyboard)

# Додайте інші хендлери для розділу Герої

# Експортуємо router як heroes_router
heroes_router = router

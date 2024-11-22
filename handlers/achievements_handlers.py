# handlers/achievements_handlers.py
from aiogram.types import Message
from aiogram import Router, F
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "🏆 Досягнення")
async def show_achievements_menu(message: Message):
    logger.info("Натиснуто кнопку '🏆 Досягнення'")
    from keyboards.achievements_menu import AchievementsMenu
    keyboard = AchievementsMenu.get_achievements_menu()
    await message.answer("Оберіть тип досягнень:", reply_markup=keyboard)

# Додайте інші хендлери для підменю Досягнень

# Експортуємо router як achievements_router
achievements_router = router

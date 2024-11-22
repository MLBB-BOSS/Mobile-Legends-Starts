# handlers/characters_handlers.py
from aiogram.types import Message
from aiogram import Router, F
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "🛡️ Танк")
async def handle_tank(message: Message):
    logger.info("Натиснуто кнопку '🛡️ Танк'")
    await message.reply("Герої класу 'Танк':\n- Герой 1\n- Герой 2", reply_markup=None)

@router.message(F.text == "🔮 Маг")
async def handle_mage(message: Message):
    logger.info("Натиснуто кнопку '🔮 Маг'")
    await message.reply("Герої класу 'Маг':\n- Герой 3\n- Герой 4", reply_markup=None)

@router.message(F.text == "🏹 Стрілець")
async def handle_archer(message: Message):
    logger.info("Натиснуто кнопку '🏹 Стрілець'")
    await message.reply("Герої класу 'Стрілець':\n- Герой 5\n- Герой 6", reply_markup=None)

@router.message(F.text == "⚔️ Асасін")
async def handle_assassin(message: Message):
    logger.info("Натиснуто кнопку '⚔️ Асасін'")
    await message.reply("Герої класу 'Асасін':\n- Герой 7\n- Герой 8", reply_markup=None)

@router.message(F.text == "🤝 Підтримка")
async def handle_support(message: Message):
    logger.info("Натиснуто кнопку '🤝 Підтримка'")
    await message.reply("Герої класу 'Підтримка':\n- Герой 9\n- Герой 10", reply_markup=None)

@router.message(F.text == "🔄 Назад")
async def handle_back_to_navigation_menu(message: Message):
    logger.info("Натиснуто кнопку '🔄 Назад' у меню персонажів")
    from keyboards.menus import NavigationMenu
    keyboard = NavigationMenu.get_navigation_menu()
    await message.answer("Повернення до меню навігації. Оберіть опцію:", reply_markup=keyboard)

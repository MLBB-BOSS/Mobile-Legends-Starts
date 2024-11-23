from aiogram import Router, F
from aiogram.types import Message
from keyboards.hero_menu import get_hero_class_menu
from keyboards.main_menu import get_main_menu
import logging

logger = logging.getLogger(__name__)
heroes_router = Router()

@heroes_router.message(F.text == "🛡️ Персонажі")
async def show_hero_classes(message: Message):
    logger.info(f"Користувач {message.from_user.id} запросив показ класів героїв")
    try:
        keyboard = get_hero_class_menu()
        await message.answer(
            "Оберіть клас героя:",
            reply_markup=keyboard
        )
    except Exception as e:
        logger.exception(f"Помилка у хендлері класів героїв: {e}")
        await message.answer(
            "Виникла помилка. Спробуйте ще раз.",
            reply_markup=get_main_menu()
        )

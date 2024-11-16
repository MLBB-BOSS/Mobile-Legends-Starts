from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from keyboards import HeroMenu
import logging

logger = logging.getLogger(__name__)
router = Router()

@router.message(Command("hero"))
async def show_hero_classes(message: Message):
    try:
        keyboard = HeroMenu.get_class_keyboard()
        await message.answer(
            "Оберіть клас героя:",
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Помилка при показі класів героїв: {e}")
        await message.answer("Вибачте, сталася помилка.")

@router.callback_query(F.data.startswith("class_"))
async def show_heroes_by_class(callback: CallbackQuery):
    try:
        hero_class = callback.data.replace("class_", "")
        keyboard = HeroMenu.get_heroes_keyboard(hero_class)
        await callback.message.edit_text(
            f"Оберіть героя класу {hero_class.title()}:",
            reply_markup=keyboard
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"Помилка при показі героїв класу: {e}")
        await callback.answer("Сталася помилка", show_alert=True)

@router.callback_query(F.data == "back_to_classes")
async def back_to_classes(callback: CallbackQuery):
    try:
        keyboard = HeroMenu.get_class_keyboard()
        await callback.message.edit_text(
            "Оберіть клас героя:",
            reply_markup=keyboard
        )
        await callback.answer()
    except Exception as e:
        logger.error(f"Помилка при поверненні до класів: {e}")
        await callback.answer("Сталася помилка", show_alert=True)

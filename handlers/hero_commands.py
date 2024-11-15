from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from services.keyboard_service import get_class_keyboard, get_heroes_keyboard
import logging

# Set up logging
logger = logging.getLogger(__name__)

# Initialize router with name
router = Router(name="hero_router")

@router.message(Command("hero"))
async def hero_command(message: Message):
    try:
        await message.answer(
            "Оберіть клас героя:", 
            reply_markup=get_class_keyboard()
        )
        logger.info(f"Hero command processed for user {message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in hero_command: {e}")
        await message.answer("Вибачте, сталася помилка. Спробуйте пізніше.")

@router.callback_query(F.data.startswith("class_"))
async def process_hero_class(callback: CallbackQuery):
    try:
        hero_class = callback.data.split("_")[1]
        keyboard = get_heroes_keyboard(hero_class)
        
        await callback.message.edit_text(
            f"Оберіть героя класу {hero_class}:",
            reply_markup=keyboard
        )
        await callback.answer()
        logger.info(f"Hero class {hero_class} processed for user {callback.from_user.id}")
    except Exception as e:
        logger.error(f"Error in process_hero_class: {e}")
        await callback.answer("Сталася помилка. Спробуйте ще раз.", show_alert=True)

@router.callback_query(F.data.startswith("hero_"))
async def process_hero_selection(callback: CallbackQuery):
    try:
        hero_name = callback.data.split("_")[1]
        await callback.message.edit_text(
            f"Інформація про героя {hero_name}:\n"
            f"[Тут буде детальна інформація про {hero_name}]"
        )
        await callback.answer()
        logger.info(f"Hero {hero_name} info requested by user {callback.from_user.id}")
    except Exception as e:
        logger.error(f"Error in process_hero_selection: {e}")
        await callback.answer("Помилка при отриманні інформації про героя.", show_alert=True)

@router.callback_query(F.data == "back_to_classes")
async def back_to_classes(callback: CallbackQuery):
    try:
        await callback.message.edit_text(
            "Оберіть клас героя:",
            reply_markup=get_class_keyboard()
        )
        await callback.answer()
        logger.info(f"Back to classes requested by user {callback.from_user.id}")
    except Exception as e:
        logger.error(f"Error in back_to_classes: {e}")
        await callback.answer("Помилка при поверненні до списку класів.", show_alert=True)

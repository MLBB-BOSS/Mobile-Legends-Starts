from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Text, Command
from services.keyboard_service import get_class_keyboard, get_heroes_keyboard

router = Router(name="hero_router")

# Command handler
@router.message(Command("hero"))
async def hero_command(message: Message):
    """Handle /hero command - shows hero class selection keyboard"""
    await message.answer(
        "Оберіть клас героя:", 
        reply_markup=get_class_keyboard()
    )

# Text message handler
@router.message(F.text.lower() == "hero")
async def hero_text(message: Message):
    """Handle 'hero' text message"""
    await hero_command(message)

# Callback handlers
@router.callback_query(Text(startswith="class_"))
async def process_hero_class(callback: CallbackQuery):
    """Handle hero class selection"""
    hero_class = callback.data.split("_")[1]
    await callback.message.edit_text(
        f"Оберіть героя класу {hero_class}:",
        reply_markup=get_heroes_keyboard(hero_class)
    )
    await callback.answer()

@router.callback_query(Text(startswith="hero_"))
async def process_hero_selection(callback: CallbackQuery):
    """Handle specific hero selection"""
    hero_name = callback.data.split("_")[1]
    await callback.message.edit_text(
        f"Інформація про героя {hero_name}:\n"
        f"[Тут буде детальна інформація про {hero_name}]"
    )
    await callback.answer()

@router.callback_query(Text(equals="back_to_classes"))
async def back_to_classes(callback: CallbackQuery):
    """Handle 'back to classes' button"""
    await callback.message.edit_text(
        "Оберіть клас героя:",
        reply_markup=get_class_keyboard()
    )
    await callback.answer()

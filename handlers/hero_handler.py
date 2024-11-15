from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from services.keyboard_service import get_class_keyboard, get_heroes_keyboard

# Важливо вказати name при створенні роутера
router = Router(name="hero_router")

@router.message(Command("start"))
async def cmd_start(message: Message):
    await message.answer("Привіт! Я бот для Mobile Legends. Використовуй /hero для вибору героя.")

@router.message(Command("hero"))
async def hero_command(message: Message):
    await message.answer(
        "Оберіть клас героя:", 
        reply_markup=get_class_keyboard()
    )

# Решта коду залишається без змін...
# Text message handler
@router.message(F.text.lower() == "hero")
async def hero_text(message: Message):
    """Handle 'hero' text message"""
    await hero_command(message)

# Callback handlers
@router.callback_query(F.data.startswith("class_"))
async def process_hero_class(callback: CallbackQuery):
    """Handle hero class selection"""
    hero_class = callback.data.split("_")[1]
    await callback.message.edit_text(
        f"Оберіть героя класу {hero_class}:",
        reply_markup=get_heroes_keyboard(hero_class)
    )
    await callback.answer()

@router.callback_query(F.data.startswith("hero_"))
async def process_hero_selection(callback: CallbackQuery):
    """Handle specific hero selection"""
    hero_name = callback.data.split("_")[1]
    await callback.message.edit_text(
        f"Інформація про героя {hero_name}:\n"
        f"[Тут буде детальна інформація про {hero_name}]"
    )
    await callback.answer()

@router.callback_query(F.data == "back_to_classes")
async def back_to_classes(callback: CallbackQuery):
    """Handle 'back to classes' button"""
    await callback.message.edit_text(
        "Оберіть клас героя:",
        reply_markup=get_class_keyboard()
    )
    await callback.answer()

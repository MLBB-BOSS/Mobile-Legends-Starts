from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
# Замість from aiogram.filters import Text тепер використовуємо F
# F.text дозволяє фільтрувати повідомлення за текстом

router = Router()

@router.message(Command("heroes"))
async def show_hero_classes(message: Message):
    """Показує меню вибору класу героїв"""
    keyboard = HeroMenu.get_class_keyboard()
    await message.answer("Виберіть клас героя:", reply_markup=keyboard)

@router.message(F.text.in_(["Tank", "Fighter", "Assassin", "Mage", "Marksman", "Support"]))
async def show_heroes_by_class(message: Message):
    """Показує героїв вибраного класу"""
    keyboard = HeroMenu.get_heroes_keyboard(message.text)
    if keyboard:
        await message.answer(f"Герої класу {message.text}:", reply_markup=keyboard)
    else:
        await message.answer("Невідомий клас героя")

@router.message(F.text == "↩️ Назад до класів")
async def back_to_classes(message: Message):
    """Повертає до меню вибору класу"""
    await show_hero_classes(message)

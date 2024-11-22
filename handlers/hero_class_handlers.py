# handlers/hero_class_handlers.py

from aiogram import Router, F
from aiogram.types import Message
from keyboards.hero_menu import get_hero_class_menu
from keyboards.navigation_menu import get_navigation_menu

hero_class_router = Router()

@hero_class_router.message(F.text.in_(["🛡️ Танк", "🔮 Маг", "🏹 Стрілець", "⚔️ Асасін", "🧬 Підтримка", "🤺 Боєць"]))
async def handle_hero_class_selection(message: Message):
    await message.answer(f"Ви обрали клас: {message.text}. Деталі цього класу ще на стадії розробки.")

@hero_class_router.message(F.text == "🔄 Назад")
async def hero_classes_back_to_navigation(message: Message):
    await message.answer("Повернення до навігації:", reply_markup=get_navigation_menu())

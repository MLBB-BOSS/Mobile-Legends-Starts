# handlers/heroes.py

from aiogram import Router, F
from aiogram.types import Message
from keyboards.heroes_menu import get_hero_class_menu
from keyboards.navigation_menu import get_navigation_menu

heroes_router = Router()

# Відображення клавіатури для героїв
@heroes_router.message(F.text == "🛡️ Персонажі")
async def show_heroes_menu(message: Message):
    """
    Відображає клавіатуру з класами героїв.
    """
    await message.answer("Оберіть клас героя:", reply_markup=get_hero_class_menu())

# Обробка вибору класу героя
@heroes_router.message(F.text.in_({"🛡️ Танк", "🔮 Маг", "🏹 Стрілець", "⚔️ Асасін", "🧬 Підтримка"}))
async def handle_hero_selection(message: Message):
    """
    Відображає відповідь для обраного класу героя.
    """
    selected_class = message.text
    await message.answer(f"Ви обрали: {selected_class}. Ця функція ще на стадії розробки.")

# Кнопка "Назад"
@heroes_router.message(F.text == "🔄 Назад")
async def back_to_navigation_menu(message: Message):
    """
    Повертає до меню навігації.
    """
    await message.answer("Повернення до меню навігації:", reply_markup=get_navigation_menu())

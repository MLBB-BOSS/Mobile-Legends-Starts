# handlers/meta.pyhandlers/meta.py

from aiogram import types, Dispatcher
from keyboards.menus import MenuButton, get_meta_menu
import logging

logger = logging.getLogger(__name__)

def register_handlers(dp: Dispatcher):
    # Обробник кнопки "🔥 META"
    @dp.message_handler(lambda message: message.text == MenuButton.META.value)
    async def meta_menu_handler(message: types.Message):
        await message.answer("Оберіть опцію META:", reply_markup=get_meta_menu())

    # Обробник кнопки "📋 Список Героїв у Мету"
    @dp.message_handler(lambda message: message.text == MenuButton.META_HERO_LIST.value)
    async def meta_hero_list_handler(message: types.Message):
        # Заглушка для відображення списку героїв у меті
        meta_heroes = [
            "Hero1", "Hero2", "Hero3"  # Замініть на реальні дані
        ]
        heroes_text = "\n".join(meta_heroes)
        await message.answer(f"Список Героїв у Мету:\n{heroes_text}", reply_markup=get_meta_menu())

    # Обробник кнопки "🌟 Рекомендації"
    @dp.message_handler(lambda message: message.text == MenuButton.META_RECOMMENDATIONS.value)
    async def meta_recommendations_handler(message: types.Message):
        # Заглушка для відображення рекомендацій
        recommendations = [
            "Рекомендація 1",
            "Рекомендація 2",
            "Рекомендація 3"
        ]
        recommendations_text = "\n".join(recommendations)
        await message.answer(f"Рекомендації:\n{recommendations_text}", reply_markup=get_meta_menu())

    # Обробник кнопки "🔄 Оновлення Мети"
    @dp.message_handler(lambda message: message.text == MenuButton.META_UPDATES.value)
    async def meta_updates_handler(message: types.Message):
        # Заглушка для відображення оновлень мети
        updates = [
            "Оновлення 1",
            "Оновлення 2",
            "Оновлення 3"
        ]
        updates_text = "\n".join(updates)
        await message.answer(f"Оновлення Мети:\n{updates_text}", reply_markup=get_meta_menu())

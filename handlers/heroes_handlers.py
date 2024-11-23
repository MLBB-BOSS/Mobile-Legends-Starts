# handlers/hero_handlers.py

from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

hero_router = Router()

@hero_router.message(F.text.in_({"🛡️ Танк", "🔮 Маг", "🏹 Стрілець", "⚔️ Асасін", "🧬 Підтримка"}))
async def show_hero_options(message: Message):
    """
    Відображає додаткові дії для обраного класу героїв.
    """
    selected_class = message.text
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Гайди", callback_data=f"guides_{selected_class}")],
            [InlineKeyboardButton(text="Контр-піки", callback_data=f"counterpicks_{selected_class}")],
            [InlineKeyboardButton(text="Білди", callback_data=f"builds_{selected_class}")]
        ]
    )
    await message.answer(f"Ви обрали {selected_class}. Що бажаєте зробити?", reply_markup=keyboard)

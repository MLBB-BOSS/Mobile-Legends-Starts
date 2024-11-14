from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from core.bot import dp  # Імпортуйте ваш диспетчер з bot.py

# Головне меню
@dp.message_handler(commands=['start'])
async def main_menu(message: types.Message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🦸 Герої", callback_data="heroes"),
        InlineKeyboardButton("📚 Інформація", callback_data="info")
    )
    await message.answer("Оберіть опцію:", reply_markup=keyboard)

# Вибір класу
@dp.callback_query_handler(Text(equals="heroes"))
async def choose_class(call: types.CallbackQuery):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("Стрілець", callback_data="class_marksman"),
        InlineKeyboardButton("Маг", callback_data="class_mage"),
        InlineKeyboardButton("Танк", callback_data="class_tank")
    )
    await call.message.edit_text("Оберіть клас героя:", reply_markup=keyboard)

# Вибір конкретного героя
@dp.callback_query_handler(Text(startswith="class_"))
async def choose_hero(call: types.CallbackQuery):
    class_name = call.data.split("_")[1]
    heroes = get_heroes_by_class(class_name)  # Функція, що повертає список героїв обраного класу
    keyboard = InlineKeyboardMarkup(row_width=3)
    for hero in heroes:
        keyboard.add(InlineKeyboardButton(hero, callback_data=f"hero_{hero}"))
    await call.message.edit_text(f"Оберіть героя класу {class_name}:", reply_markup=keyboard)

# Вибір дії для героя
@dp.callback_query_handler(Text(startswith="hero_"))
async def hero_options(call: types.CallbackQuery):
    hero_name = call.data.split("_")[1]
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("ℹ️ Загальна інформація", callback_data=f"info_{hero_name}"),
        InlineKeyboardButton("📖 Гайди", callback_data=f"guides_{hero_name}"),
        InlineKeyboardButton("🎯 Контрпіки", callback_data=f"counter_{hero_name}")
    )
    await call.message.edit_text(f"Ви обрали героя {hero_name}. Оберіть опцію:", reply_markup=keyboard)

# Функція для отримання списку героїв (потрібно реалізувати)
def get_heroes_by_class(class_name):
    # Повертайте список героїв у вигляді списку строк на основі класу
    return ["Beatrix", "Brody", "Bruno"]  # Примерний список

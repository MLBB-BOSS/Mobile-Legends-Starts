from aiogram import types
from aiogram.types import InputFile, InlineKeyboardMarkup, InlineKeyboardButton
from utils.charts import generate_activity_chart
from utils.db import get_user_profile  # Функція для отримання даних користувача
from loader import dp, bot  # Основні інстанси бота

async def send_user_profile(chat_id, user_data):
    """
    Відправляє профіль користувача з графіком.
    """
    chart = generate_activity_chart(user_data)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("🔄 Оновити", callback_data="refresh_profile"))

    await bot.send_photo(
        chat_id=chat_id,
        photo=InputFile(chart, filename="profile_chart.png"),
        caption=(
            f"🔍 **Ваш Профіль**:\n"
            f"👤 Ім'я користувача: @{user_data['username']}\n"
            f"🚀 Рейтинг: {user_data['rating']}\n"
            f"🎮 Матчі: {user_data['matches']}, Перемоги: {user_data['wins']}, Поразки: {user_data['losses']}"
        ),
        reply_markup=markup
    )

@dp.callback_query_handler(lambda c: c.data == 'my_profile')
async def profile_callback(callback_query: types.CallbackQuery):
    """
    Обробник для кнопки 'Мій профіль'.
    """
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    user_data = get_user_profile(user_id)  # Отримуємо дані користувача
    await send_user_profile(callback_query.message.chat.id, user_data)

@dp.callback_query_handler(lambda c: c.data == 'refresh_profile')
async def refresh_profile_callback(callback_query: types.CallbackQuery):
    """
    Оновлює дані профілю користувача.
    """
    await bot.answer_callback_query(callback_query.id, text="🔄 Оновлення профілю...")
    user_id = callback_query.from_user.id
    user_data = get_user_profile(user_id)
    await send_user_profile(callback_query.message.chat.id, user_data)

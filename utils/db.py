import shutil

# Update project files programmatically
# Step 1: Define updates for files
updates = {
    'utils/db.py': '''import sqlite3

def get_user_profile(user_id):
    \"\"\"
    Отримує дані профілю користувача з бази даних.
    :param user_id: Telegram ID користувача.
    :return: Словник з даними користувача.
    \"\"\"
    connection = sqlite3.connect("database.db")  # Підключення до бази даних
    cursor = connection.cursor()

    cursor.execute(\"""
        SELECT username, rating, matches, wins, losses
        FROM users
        WHERE telegram_id = ?
    \""", (user_id,))
    
    result = cursor.fetchone()
    connection.close()

    if result:
        return {
            "username": result[0],
            "rating": result[1],
            "matches": result[2],
            "wins": result[3],
            "losses": result[4],
            "sessions": [1, 2, 3, 4, 5],
            "ratings": [100, 120, 150, 180, 210]
        }
    else:
        return {
            "username": "unknown",
            "rating": 0,
            "matches": 0,
            "wins": 0,
            "losses": 0,
            "sessions": [0],
            "ratings": [0]
        }
''',

    'utils/charts.py': '''import matplotlib.pyplot as plt
import io

def generate_activity_chart(user_data):
    \"\"\"
    Генерує графік активності користувача.
    :param user_data: Словник з даними користувача (sessions, ratings).
    :return: BytesIO зображення графіку.
    \"\"\"
    sessions = user_data['sessions']
    ratings = user_data['ratings']

    plt.figure(figsize=(6, 4))
    plt.plot(sessions, ratings, marker='o', linestyle='-', linewidth=2)
    plt.title('Графік зміни рейтингу')
    plt.xlabel('Сеанс')
    plt.ylabel('Рейтинг')
    plt.grid(True)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()
    return buf
''',

    'handlers/profile.py': '''from aiogram import types
from aiogram.types import InputFile, InlineKeyboardMarkup, InlineKeyboardButton
from utils.charts import generate_activity_chart
from utils.db import get_user_profile
from loader import dp, bot

async def send_user_profile(chat_id, user_data):
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
    await bot.answer_callback_query(callback_query.id)
    user_id = callback_query.from_user.id
    user_data = get_user_profile(user_id)
    await send_user_profile(callback_query.message.chat.id, user_data)

@dp.callback_query_handler(lambda c: c.data == 'refresh_profile')
async def refresh_profile_callback(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id, text="🔄 Оновлення профілю...")
    user_id = callback_query.from_user.id
    user_data = get_user_profile(user_id)
    await send_user_profile(callback_query.message.chat.id, user_data)
''',

    'keyboards/inline_menus.py': '''from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🪪 Мій Профіль", callback_data="my_profile")],
        [InlineKeyboardButton(text="🧭 Навігація", callback_data="navigation")]
    ])
''',
}

# Step 2: Write updates to corresponding files
for relative_path, content in updates.items():
    file_path = os.path.join(extract_path, "Mobile-Legends-Starts-aiogram-3x", relative_path)
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)

# Step 3: Repack the updated project into a ZIP file
output_zip_path = '/mnt/data/updated_mobile_legends_aiogram.zip'
shutil.make_archive('/mnt/data/updated_mobile_legends_aiogram', 'zip', extract_path)

output_zip_path

from aiogram import Router, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

router = Router()

# Звичайна клавіатура
def main_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton("📊 Статистика"), KeyboardButton("🏆 Досягнення")],
            [KeyboardButton("⚙️ Налаштування"), KeyboardButton("❓ Допомога")],
        ],
        resize_keyboard=True
    )

# Інлайн-клавіатура для статистики
def statistics_inline():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎯 Загальна Активність", callback_data="general_activity")],
        [InlineKeyboardButton(text="🎮 Ігрова Статистика", callback_data="game_stats")],
        [InlineKeyboardButton(text="📈 Графік Активності", callback_data="activity_chart")],
        [InlineKeyboardButton(text="🔙 Назад", callback_data="main_menu")]
    ])

# Обробник для головного меню
@router.message(lambda message: message.text == "/start" or message.text == "🔙 Назад")
async def show_main_menu(message: types.Message):
    await message.delete()
    await message.answer("🗂 *Головне меню*", reply_markup=main_menu(), parse_mode="Markdown")
    await message.answer("📊 Виберіть категорію для перегляду статистики:", reply_markup=statistics_inline())

# Обробник для інлайн-кнопок
@router.callback_query(lambda c: c.data == "activity_chart")
async def send_activity_chart(callback: types.CallbackQuery):
    import matplotlib.pyplot as plt
    import io

    # Генерація графіка
    x = [1, 2, 3, 4, 5]
    y = [100, 120, 160, 200, 220]

    plt.plot(x, y, marker="o", color="b")
    plt.title("Графік активності")
    plt.xlabel("Сеанс")
    plt.ylabel("Рейтинг")
    plt.grid()

    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    plt.close()

    # Редагування інлайн-повідомлення
    await callback.message.edit_media(
        types.InputMediaPhoto(media=buffer, caption="📈 Ваш графік активності"),
        reply_markup=statistics_inline()

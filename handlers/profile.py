from aiogram import Router, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import matplotlib.pyplot as plt
import io

router = Router()

# Клавіатура для навігації профілю
def profile_inline_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton("📊 Загальна Статистика", callback_data="general_stats")],
        [InlineKeyboardButton("📈 Графік Активності", callback_data="activity_chart")],
        [InlineKeyboardButton("🔄 Оновити", callback_data="refresh_profile")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main")]
    ])

# Обробник для кнопки "Мій Профіль"
@router.message(lambda message: message.text == "👤 Мій профіль")
async def show_profile(message: types.Message):
    await message.delete()
    await message.answer("🔍 *Ваш Профіль:*\n\nЗавантаження статистики...", 
                         reply_markup=profile_inline_menu(), parse_mode="Markdown")

# Загальна статистика
@router.callback_query(lambda c: c.data == "general_stats")
async def show_general_stats(callback: types.CallbackQuery):
    text = (
        "📊 *Загальна Статистика:*\n"
        "- 🧩 Вікторини: 10\n"
        "- 🎯 Місії: 20\n"
        "- 🏆 Рейтинг: Топ-25\n"
        "- 💬 Повідомлень: 250"
    )
    await callback.message.edit_text(text, reply_markup=profile_inline_menu(), parse_mode="Markdown")

# Графік активності
@router.callback_query(lambda c: c.data == "activity_chart")
async def send_activity_chart(callback: types.CallbackQuery):
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

    await callback.message.answer_photo(photo=buffer, caption="📈 Ваш графік активності", 
                                        reply_markup=profile_inline_menu())

# Оновлення профілю
@router.callback_query(lambda c: c.data == "refresh_profile")
async def refresh_profile(callback: types.CallbackQuery):
    await callback.answer("🔄 Оновлення даних...")
    await show_profile(callback.message)

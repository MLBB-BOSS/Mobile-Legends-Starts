from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

router = Router()

# Клавіатура другого рівня для Профілю
def get_profile_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📈 Статистика"), KeyboardButton(text="⚙️ Налаштування")],
            [KeyboardButton(text="💌 Зворотний зв'язок"), KeyboardButton(text="🔙 Назад")],
        ],
        resize_keyboard=True
    )

@router.message(F.text == "🪪 Профіль")
async def handle_profile(message: Message):
    await message.answer(
        "Це розділ профілю. Оберіть опцію:",
        reply_markup=get_profile_keyboard()
    )

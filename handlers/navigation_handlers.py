from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton

router = Router()

# Клавіатура другого рівня для Навігації
def get_navigation_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🛡️ Персонажі"), KeyboardButton(text="📚 Гайди")],
            [KeyboardButton(text="⚔️ Контр-піки"), KeyboardButton(text="⚜️ Білди")],
            [KeyboardButton(text="🔙 Назад")],
        ],
        resize_keyboard=True
    )

@router.message(F.text == "🧭 Навігація")
async def handle_navigation(message: Message):
    await message.answer(
        "Це розділ навігації. Оберіть опцію:",
        reply_markup=get_navigation_keyboard()
    )

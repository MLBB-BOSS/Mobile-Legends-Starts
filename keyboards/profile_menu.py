from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_profile_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text="📈 Статистика"),
            KeyboardButton(text="🏆 Досягнення"),
            KeyboardButton(text="💌 Зворотний Зв'язок")
        ],
        [
            KeyboardButton(text="⚙️ Налаштування"),
            KeyboardButton(text="❓ Допомога"),
            KeyboardButton(text="🔙 Назад до Головного")
        ]
    ]
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Оберіть опцію профілю"
    )
    return keyboard

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_characters_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text="🗡️ Бійці"),
            KeyboardButton(text="🏹 Стрільці")
        ],
        [
            KeyboardButton(text="🔮 Маги"),
            KeyboardButton(text="🛡️ Танки")
        ],
        [
            KeyboardButton(text="🏥 Саппорти"),
            KeyboardButton(text="🗲 Гібриди")
        ],
        [
            KeyboardButton(text="🔙 Назад до Навігації")
        ]
    ]
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
        input_field_placeholder="Оберіть тип героя"
    )
    
    return keyboard

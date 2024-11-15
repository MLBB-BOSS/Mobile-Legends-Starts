from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard() -> ReplyKeyboardMarkup:
    # Створюємо кнопки
    keyboard = [
        [
            KeyboardButton(text="🦸‍♂️ Герої"),
            KeyboardButton(text="🎯 Мета")
        ],
        [
            KeyboardButton(text="🛠️ Білди"),
            KeyboardButton(text="❓ Допомога")
        ]
    ]
    
    # Створюємо клавіатуру з кнопками
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,  # Зменшує розмір кнопок
        input_field_placeholder="Оберіть опцію..."  # Підказка в полі вводу
    )

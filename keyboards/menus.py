from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Налаштування логування
import logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

# Головна клавіатура (ReplyKeyboardMarkup)
def get_main_reply_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🧭 Навігація"),
                KeyboardButton(text="🪪 Мій Профіль")
            ]
        ],
        resize_keyboard=True
    )

# Клавіатура для навігації (ReplyKeyboardMarkup)
def get_navigation_reply_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🥷 Персонажі"),
                KeyboardButton(text="🛡️ Білди")
            ],
            [
                KeyboardButton(text="⚖️ Контр-піки"),
                KeyboardButton(text="📊 Голосування")
            ],
            [
                KeyboardButton(text="📚 Гайди"),
                KeyboardButton(text="🏆 M6")
            ],
            [
                KeyboardButton(text="🔥 META"),
                KeyboardButton(text="🔙 Назад")
            ]
        ],
        resize_keyboard=True
    )

# Клавіатура для персонажів (ReplyKeyboardMarkup)
def get_heroes_reply_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🛡️ Танк"),
                KeyboardButton(text="🧙‍♂️ Маг")
            ],
            [
                KeyboardButton(text="🏹 Стрілець"),
                KeyboardButton(text="⚔️ Асасін")
            ],
            [
                KeyboardButton(text="❤️ Підтримка"),
                KeyboardButton(text="🗡️ Боєць")
            ],
            [
                KeyboardButton(text="🔎 Пошук"),
                KeyboardButton(text="🔙 Назад")
            ]
        ],
        resize_keyboard=True
    )

# Клавіатура для гайдів (ReplyKeyboardMarkup)
def get_guides_reply_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🆕 Нові Гайди"),
                KeyboardButton(text="🌟 Топ Гайди")
            ],
            [
                KeyboardButton(text="📘 Для Початківців"),
                KeyboardButton(text="🧙 Стратегії гри")
            ],
            [
                KeyboardButton(text="🤝 Командна Гра"),
                KeyboardButton(text="🔙 Назад")
            ]
        ],
        resize_keyboard=True
    )

# Клавіатура для профілю (ReplyKeyboardMarkup)
def get_profile_reply_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="📈 Статистика"),
                KeyboardButton(text="🏆 Досягнення")
            ],
            [
                KeyboardButton(text="⚙️ Налаштування"),
                KeyboardButton(text="💌 Зворотний Зв'язок")
            ],
            [
                KeyboardButton(text="❓ Допомога"),
                KeyboardButton(text="🔙 Назад до Головного Меню")
            ]
        ],
        resize_keyboard=True
    )

# Додаткові клавіатури можна додати аналогічно

# Тестування
if __name__ == "__main__":
    logging.info("Головна клавіатура:")
    print(get_main_reply_keyboard().keyboard)

    logging.info("Клавіатура Навігації:")
    print(get_navigation_reply_keyboard().keyboard)

    logging.info("Клавіатура Персонажів:")
    print(get_heroes_reply_keyboard().keyboard)

    logging.info("Клавіатура Гайдів:")
    print(get_guides_reply_keyboard().keyboard)

    logging.info("Клавіатура Профілю:")
    print(get_profile_reply_keyboard().keyboard)

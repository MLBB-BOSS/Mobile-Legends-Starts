from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_second_level_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text="🥷 Персонажі"),
            KeyboardButton(text="⚙️ Білди"),
            KeyboardButton(text="📈 Мета")
        ],
        [
            KeyboardButton(text="📚 Гайди"),
            KeyboardButton(text="🏆 Турніри"),
            KeyboardButton(text="💡 Стратегії")
        ],
        [
            KeyboardButton(text="🎮 Механіки гри"),
            KeyboardButton(text="📢 Новини"),
            KeyboardButton(text="🔙 Назад")
        ]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard

def get_guides_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text="🆕 Нові гайди"),
            KeyboardButton(text="⭐ Популярні гайди"),
            KeyboardButton(text="📘 Для початківців")
        ],
        [
            KeyboardButton(text="🧙 Просунуті техніки"),
            KeyboardButton(text="🛡️ Командні стратегії"),
            KeyboardButton(text="◀️ Назад до Навігації")
        ]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard

def get_counterpicks_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text="🔍 Пошук контр-піку"),
            KeyboardButton(text="📜 Список персонажів"),
            KeyboardButton(text="🏆 Топ контр-піки")
        ],
        [KeyboardButton(text="◀️ Назад до Навігації")]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard

def get_builds_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text="🔧 Створити білд"),
            KeyboardButton(text="📄 Мої білди"),
            KeyboardButton(text="⭐ Популярні білди")
        ],
        [
            KeyboardButton(text="🔍 Порівняння білдів"),
            KeyboardButton(text="◀️ Назад до Навігації")
        ]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard

def get_characters_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text="🗡️ Бійці"),
            KeyboardButton(text="🏹 Стрільці"),
            KeyboardButton(text="🔮 Маги")
        ],
        [
            KeyboardButton(text="🛡️ Танки"),
            KeyboardButton(text="🏥 Саппорти"),
            KeyboardButton(text="⚔️ Гібриди")
        ],
        [
            KeyboardButton(text="🔥 Метові"),
            KeyboardButton(text="◀️ Назад до Навігації")
        ]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard

def get_voting_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text="🗳️ Нове голосування"),
            KeyboardButton(text="📊 Мої голосування"),
            KeyboardButton(text="⭐ Популярні голосування")
        ],
        [
            KeyboardButton(text="🔍 Пошук голосування"),
            KeyboardButton(text="◀️ Назад до Навігації")
        ]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard

def get_help_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text="❓ FAQ"),
            KeyboardButton(text="📞 Підтримка"),
            KeyboardButton(text="📝 Надіслати відгук")
        ],
        [
            KeyboardButton(text="◀️ Назад до Навігації")
        ]
    ]
    keyboard = ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)
    return keyboard

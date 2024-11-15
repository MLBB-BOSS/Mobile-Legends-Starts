from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_class_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [
            InlineKeyboardButton(text="Tank", callback_data="class_tank"),
            InlineKeyboardButton(text="Fighter", callback_data="class_fighter")
        ],
        [
            InlineKeyboardButton(text="Assassin", callback_data="class_assassin"),
            InlineKeyboardButton(text="Mage", callback_data="class_mage")
        ],
        [
            InlineKeyboardButton(text="Marksman", callback_data="class_marksman"),
            InlineKeyboardButton(text="Support", callback_data="class_support")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_heroes_keyboard(hero_class: str) -> InlineKeyboardMarkup:
    heroes = {
        "tank": ["Tigreal", "Franco", "Minotaur"],
        "fighter": ["Alucard", "Zilong", "Balmond"],
        "assassin": ["Saber", "Fanny", "Karina"],
        "mage": ["Eudora", "Gord", "Aurora"],
        "marksman": ["Layla", "Miya", "Bruno"],
        "support": ["Rafaela", "Estes", "Angela"]
    }
    
    buttons = []
    for hero in heroes.get(hero_class.lower(), []):
        buttons.append([
            InlineKeyboardButton(text=hero, callback_data=f"hero_{hero}")
        ])
    
    buttons.append([
        InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_classes")
    ])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

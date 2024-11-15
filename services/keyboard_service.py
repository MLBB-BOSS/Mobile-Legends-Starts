from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_class_keyboard() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
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
    ])
    return keyboard

def get_heroes_keyboard(hero_class: str) -> InlineKeyboardMarkup:
    # Тут можна додати реальних героїв для кожного класу
    heroes = {
        "tank": ["Tigreal", "Franco", "Minotaur"],
        "fighter": ["Alucard", "Zilong", "Balmond"],
        # Додайте інших героїв для інших класів
    }
    
    buttons = []
    for hero in heroes.get(hero_class.lower(), []):
        buttons.append([InlineKeyboardButton(text=hero, callback_data=f"hero_{hero}")])
    
    buttons.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_classes")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)

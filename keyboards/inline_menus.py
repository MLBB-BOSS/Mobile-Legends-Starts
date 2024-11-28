# keyboards/inline_menus.py

def get_hero_class_inline_keyboard(hero_class: str) -> InlineKeyboardMarkup:
    """
    Створює інлайн-клавіатуру для вибору героя з певного класу.
    
    :param hero_class: Клас героя (наприклад, "Танк", "Маг" і т.д.)
    :return: InlineKeyboardMarkup
    """
    # Приклад для демонстрації. Замініть на реальні герої та їхні callback_data
    heroes_inline_keyboard = {
        "Танк": [
            InlineKeyboardButton(text="Tigreal", callback_data="hero_tigreal"),
            InlineKeyboardButton(text="Franco", callback_data="hero_franco"),
            InlineKeyboardButton(text="Minotaur", callback_data="hero_minotaur")
        ],
        "Маг": [
            InlineKeyboardButton(text="Lunox", callback_data="hero_lunox"),
            InlineKeyboardButton(text="Vale", callback_data="hero_vale"),
            InlineKeyboardButton(text="Kadita", callback_data="hero_kadita")
        ],
        # Додайте інші класи та героїв за необхідності
    }
    
    buttons = heroes_inline_keyboard.get(hero_class, [])
    
    # Розміщуємо кнопки по 2 в ряд
    keyboard = [
        buttons[i:i + 2] for i in range(0, len(buttons), 2)
    ]
    
    # Додаємо кнопку "Назад"
    keyboard.append([InlineKeyboardButton(text="🔄 Назад", callback_data=CallbackData.BACK.value)])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

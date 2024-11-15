from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_class_keyboard():
    """Повертає клавіатуру для вибору класу героїв."""
    # В aiogram 3.x використовуємо inline_keyboard для створення розмітки
    classes = ["Assassin", "Fighter", "Mage", "Marksman", "Support", "Tank"]
    keyboard = []
    
    # Створюємо кнопки по одній в рядку
    for hero_class in classes:
        keyboard.append([
            InlineKeyboardButton(text=hero_class, callback_data=f"class_{hero_class}")
        ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_heroes_keyboard(hero_class):
    """Повертає клавіатуру для вибору героя з певного класу."""
    # Список героїв для кожного класу може бути збережений у файлах або базі даних
    heroes = ["Hero1", "Hero2", "Hero3"]  # Приклад героїв
    keyboard = []
    
    # Створюємо кнопки для героїв
    for hero in heroes:
        keyboard.append([
            InlineKeyboardButton(text=hero, callback_data=f"hero_{hero}")
        ])
    
    # Додаємо кнопку "Назад"
    keyboard.append([
        InlineKeyboardButton(text="Назад", callback_data="back_to_classes")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

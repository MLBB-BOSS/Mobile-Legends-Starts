def get_hero_class_menu(hero_classes: list[str]) -> ReplyKeyboardMarkup:
    keyboard = [[KeyboardButton(text=hero)] for hero in hero_classes]
    keyboard.append([KeyboardButton(text="🔄 Назад")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

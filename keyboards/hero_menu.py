from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

class HeroMenu:
    def get_hero_classes_menu(self) -> ReplyKeyboardMarkup:
        buttons = [
            [KeyboardButton(text="🛡️ Танк"), KeyboardButton(text="🔮 Маг")],
            [KeyboardButton(text="🏹 Стрілець"), KeyboardButton(text="⚔️ Асасін")],
            [KeyboardButton(text="🔙 Назад до меню")]
        ]
        return ReplyKeyboardMarkup(
            keyboard=buttons,
            resize_keyboard=True,
            one_time_keyboard=True
        )

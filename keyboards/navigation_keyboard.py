# File: keyboards/navigation_keyboard.py
from .base_keyboard import BaseKeyboard

class NavigationKeyboard(BaseKeyboard):
    def get_navigation_menu(self) -> ReplyKeyboardMarkup:
        buttons = [
            "👥 Персонажі",
            "📖 Гайди",
            "⚔️ Контр-піки",
            "🛠️ Білди",
            "📊 Голосування",
            "🔙 Назад до Головного меню"
        ]
        return self.create_markup(buttons, row_width=2)

    def get_characters_menu(self) -> ReplyKeyboardMarkup:
        buttons = [
            "🔍 Пошук Персонажа",
            "🛡️ Танк",
            "🔮 Маг",
            "🏹 Стрілець",
            "🗡️ Асасін",
            "🛠️ Підтримка",
            "🔙 Назад до Навігації"
        ]
        return self.create_markup(buttons, row_width=2)

    def get_guides_menu(self) -> ReplyKeyboardMarkup:
        buttons = [
            "🆕 Нові Гайди",
            "⭐ Популярні Гайди",
            "🧑‍🏫 Для Початківців",
            "🧙‍♂️ Просунуті Техніки",
            "⚔️ Стратегії Командної Гри",
            "🔙 Назад до Навігації"
        ]
        return self.create_markup(buttons, row_width=2)

    # Add other navigation submenus...

# keyboards/menu_keyboards.py
# Created: 2024-11-24
# Author: MLBB-BOSS
# Description: Клавіатури для головного меню та підменю

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class NavigationKeyboards:
    @staticmethod
    def main_navigation() -> InlineKeyboardMarkup:
        """Створює клавіатуру для розділу 'Навігація'"""
        keyboard = InlineKeyboardMarkup(row_width=1)
        
        # Кнопки першого рівня навігації
        keyboard.add(
            InlineKeyboardButton(text="🛡️ Персонажі", callback_data="nav_heroes"),
            InlineKeyboardButton(text="📖 Гайди", callback_data="nav_guides"),
            InlineKeyboardButton(text="⚔️ Контр-піки", callback_data="nav_counterpicks"),
            InlineKeyboardButton(text="🛠️ Білди", callback_data="nav_builds"),
            InlineKeyboardButton(text="🔙 Назад до головного меню", callback_data="main_menu")
        )
        return keyboard

    @staticmethod
    def heroes_submenu() -> InlineKeyboardMarkup:
        """Створює підменю для розділу 'Персонажі'"""
        keyboard = InlineKeyboardMarkup(row_width=2)
        
        # Кнопки для вибору класу героя
        buttons = [
            ("🔍 Пошук персонажа", "hero_search"),
            ("🛡️ Танк", "hero_tank"),
            ("🔮 Маг", "hero_mage"),
            ("🏹 Стрілець", "hero_marksman"),
            ("🗡️ Асасін", "hero_assassin"),
            ("🤝 Підтримка", "hero_support")
        ]
        
        # Додаємо кнопки попарно
        for i in range(0, len(buttons), 2):
            row_buttons = [
                InlineKeyboardButton(text=buttons[i][0], callback_data=buttons[i][1])
            ]
            if i + 1 < len(buttons):
                row_buttons.append(
                    InlineKeyboardButton(
                        text=buttons[i+1][0], 
                        callback_data=buttons[i+1][1]
                    )
                )
            keyboard.row(*row_buttons)
            
        # Кнопка повернення
        keyboard.add(
            InlineKeyboardButton(
                text="🔙 Назад до навігації", 
                callback_data="nav_main"
            )
        )
        return keyboard

class ProfileKeyboards:
    @staticmethod
    def main_profile() -> InlineKeyboardMarkup:
        """Створює клавіатуру для розділу 'Мій профіль'"""
        keyboard = InlineKeyboardMarkup(row_width=1)
        
        # Основні розділи профілю
        keyboard.add(
            InlineKeyboardButton(text="📈 Статистика", callback_data="profile_stats"),
            InlineKeyboardButton(text="🏅 Досягнення", callback_data="profile_achievements"),
            InlineKeyboardButton(text="⚙️ Налаштування", callback_data="profile_settings"),
            InlineKeyboardButton(text="💌 Зворотний зв'язок", callback_data="profile_feedback"),
            InlineKeyboardButton(text="🔙 Назад до головного меню", callback_data="main_menu")
        )
        return keyboard

    @staticmethod
    def stats_submenu() -> InlineKeyboardMarkup:
        """Створює підменю для розділу 'Статистика'"""
        keyboard = InlineKeyboardMarkup(row_width=1)
        
        keyboard.add(
            InlineKeyboardButton(text="📊 Загальна активність", callback_data="stats_activity"),
            InlineKeyboardButton(text="🥇 Рейтинг", callback_data="stats_rating"),
            InlineKeyboardButton(text="🎮 Ігрова статистика", callback_data="stats_game"),
            InlineKeyboardButton(text="🔙 Назад до профілю", callback_data="profile_main")
        )
        return keyboard

    @staticmethod
    def settings_submenu() -> InlineKeyboardMarkup:
        """Створює підменю для розділу 'Налаштування'"""
        keyboard = InlineKeyboardMarkup(row_width=1)
        
        keyboard.add(
            InlineKeyboardButton(text="🌐 Мова інтерфейсу", callback_data="settings_language"),
            InlineKeyboardButton(text="🆔 Змінити Username", callback_data="settings_username"),
            InlineKeyboardButton(text="🎯 Оновити ID гравця", callback_data="settings_game_id"),
            InlineKeyboardButton(text="🔔 Налаштування сповіщень", callback_data="settings_notifications"),
            InlineKeyboardButton(text="🔙 Назад до профілю", callback_data="profile_main")
        )
        return keyboard

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

class BaseKeyboard:
    """Base class for all keyboards"""
    
    def create_reply_markup(
        self,
        keyboard: list[list[str]],
        resize_keyboard: bool = True,
        one_time_keyboard: bool = False
    ) -> ReplyKeyboardMarkup:
        """
        Creates a reply keyboard markup from a list of button texts
        
        Args:
            keyboard: List of lists of button texts
            resize_keyboard: Whether to resize the keyboard
            one_time_keyboard: Whether to hide keyboard after first use
        """
        markup = ReplyKeyboardMarkup(
            resize_keyboard=resize_keyboard,
            one_time_keyboard=one_time_keyboard
        )
        
        for row in keyboard:
            markup.row(*[KeyboardButton(text=button) for button in row])
            
        return markup


class MainKeyboard(BaseKeyboard):
    """Class for main keyboard functionalities"""

    def get_main_menu(self) -> ReplyKeyboardMarkup:
        """Creates main menu keyboard"""
        keyboard = [
            ["🧭 Навігація", "🎯 Герої"],
            ["🪪 Профіль", "⚙️ Налаштування"],
            ["🎫 Купити білети", "📊 Статистика"]
        ]
        return self.create_reply_markup(keyboard)

    def get_navigation_menu(self) -> ReplyKeyboardMarkup:
        """Creates navigation menu keyboard"""
        keyboard = [
            ["👥 Персонажі", "🗺 Мапи"],
            ["🏆 Турніри", "📖 Гайди"],
            ["🔙 Назад до Головного меню"]
        ]
        return self.create_reply_markup(keyboard)

    def get_heroes_menu(self) -> ReplyKeyboardMarkup:
        """Creates heroes menu keyboard"""
        keyboard = [
            ["🛡️ Танк", "🔮 Маг", "🏹 Стрілець"],
            ["🗡️ Асасін", "🛠️ Підтримка"],
            ["🔍 Пошук Персонажа"],
            ["🔙 Назад до Головного меню"]
        ]
        return self.create_reply_markup(keyboard)

    def get_profile_menu(self) -> ReplyKeyboardMarkup:
        """Creates profile menu keyboard"""
        keyboard = [
            ["📊 Статистика", "🏆 Досягнення"],
            ["📸 Мої скріншоти", "📝 Мої замітки"],
            ["🔙 Назад до Головного меню"]
        ]
        return self.create_reply_markup(keyboard)

    def get_settings_menu(self) -> ReplyKeyboardMarkup:
        """Creates settings menu keyboard"""
        keyboard = [
            ["🔔 Сповіщення", "🌐 Мова"],
            ["👤 Профіль", "❌ Видалити дані"],
            ["🔙 Назад до Головного меню"]
        ]
        return self.create_reply_markup(keyboard)

    def get_tournament_menu(self) -> ReplyKeyboardMarkup:
        """Creates tournament menu keyboard"""
        keyboard = [
            ["📝 Реєстрація", "🏆 Активні турніри"],
            ["📊 Рейтинг", "📜 Правила"],
            ["🔙 Назад до Головного меню"]
        ]
        return self.create_reply_markup(keyboard)

    def get_ticket_menu(self) -> ReplyKeyboardMarkup:
        """Creates ticket purchase menu keyboard"""
        keyboard = [
            ["🎫 Купити білет", "🎁 Промокод"],
            ["📋 Мої білети", "📜 Умови"],
            ["🔙 Назад до Головного меню"]
        ]
        return self.create_reply_markup(keyboard)


class InlineKeyboard:
    """Class for inline keyboard functionalities"""

    def create_inline_markup(self, buttons: list[list[tuple[str, str]]]) -> InlineKeyboardMarkup:
        """
        Creates an inline keyboard markup from a list of button tuples
        
        Args:
            buttons: List of lists of (text, callback_data) tuples
        """
        markup = InlineKeyboardMarkup()
        
        for row in buttons:
            markup.row(*[InlineKeyboardButton(
                text=button[0],
                callback_data=button[1]
            ) for button in row])
            
        return markup

    def get_hero_info_keyboard(self, hero_id: str) -> InlineKeyboardMarkup:
        """Creates inline keyboard for hero information"""
        buttons = [
            [("📊 Статистика", f"hero_stats_{hero_id}"), ("🎯 Навички", f"hero_skills_{hero_id}")],
            [("🛠️ Спорядження", f"hero_items_{hero_id}"), ("📖 Гайд", f"hero_guide_{hero_id}")],
            [("🔙 Назад", "back_to_heroes")]
        ]
        return self.create_inline_markup(buttons)

    def get_tournament_info_keyboard(self, tournament_id: str) -> InlineKeyboardMarkup:
        """Creates inline keyboard for tournament information"""
        buttons = [
            [("📝 Зареєструватися", f"register_{tournament_id}")],
            [("📊 Таблиця", f"standings_{tournament_id}"), ("📜 Правила", f"rules_{tournament_id}")],
            [("🔙 Назад", "back_to_tournaments")]
        ]
        return self.create_inline_markup(buttons)

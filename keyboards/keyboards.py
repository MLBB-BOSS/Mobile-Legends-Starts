# Consolidated keyboards

# From inline_keyboard.py
# keyboards/inline_keyboard.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

class InlineKeyboard:
    def create_inline_markup(self, buttons: list[list[tuple[str, str]]]) -> InlineKeyboardMarkup:
        markup = InlineKeyboardMarkup()
        
        for row in buttons:
            markup.row(*[InlineKeyboardButton(
                text=button[0],
                callback_data=button[1]
            ) for button in row])
            
        return markup

    # Інші методи...


# From keyboard_utils.py
# File: keyboards/keyboard_utils.py

from aiogram.types import InlineKeyboardButton
from typing import List, Union, Dict

def create_keyboard_row(*buttons: Union[Dict, InlineKeyboardButton]) -> List[InlineKeyboardButton]:
    """
    Створює ряд кнопок з словників або готових кнопок

    :param buttons: Кнопки у вигляді словників або об'єктів InlineKeyboardButton
    :return: Список кнопок InlineKeyboardButton
    """
    row = []
    for button in buttons:
        if isinstance(button, dict):
            row.append(InlineKeyboardButton(**button))
        elif isinstance(button, InlineKeyboardButton):
            row.append(button)
    return row


# From menu_states.py
# File: keyboards/menu_states.py
from enum import Enum, auto

class MenuState(Enum):
    MAIN = auto()
    NAVIGATION = auto()
    PROFILE = auto()
    
    # Navigation submenu states
    CHARACTERS = auto()
    GUIDES = auto()
    COUNTER_PICKS = auto()
    BUILDS = auto()
    VOTING = auto()
    
    # Profile submenu states
    STATISTICS = auto()
    ACHIEVEMENTS = auto()
    SETTINGS = auto()
    FEEDBACK = auto()
    HELP = auto()


# From navigation_menu.py
# File: keyboards/navigation_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)

class NavigationMenu:
    def get_main_navigation(self) -> ReplyKeyboardMarkup:
        """Creates and returns the main navigation menu keyboard"""
        try:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=loc.get_message("buttons.guides") or "📖 Гайди"),
                        KeyboardButton(text=loc.get_message("buttons.characters") or "👥 Персонажі")
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.counter_picks") or "⚔️ Контр-піки"),
                        KeyboardButton(text=loc.get_message("buttons.builds") or "🛠️ Білди")
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.voting") or "📊 Голосування")
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.back") or "↩️ Назад")
                    ]
                ],
                resize_keyboard=True
            )
            return keyboard
        except Exception as e:
            logger.error(f"Помилка створення навігаційного меню: {e}")
            # Return a simplified fallback keyboard
            return ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="↩️ Назад")]
                ],
                resize_keyboard=True
            )

    def get_heroes_menu(self) -> ReplyKeyboardMarkup:
        """Creates and returns the heroes menu keyboard"""
        try:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=loc.get_message("heroes.classes.tank.name") or "Танк"),
                        KeyboardButton(text=loc.get_message("heroes.classes.fighter.name") or "Бійці")
                    ],
                    [
                        KeyboardButton(text=loc.get_message("heroes.classes.assassin.name") or "Асасини"),
                        KeyboardButton(text=loc.get_message("heroes.classes.mage.name") or "Маги")
                    ],
                    [
                        KeyboardButton(text=loc.get_message("heroes.classes.marksman.name") or "Стрільці"),
                        KeyboardButton(text=loc.get_message("heroes.classes.support.name") or "Підтримка")
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.back_to_navigation") or "↩️ До навігації")
                    ]
                ],
                resize_keyboard=True
            )
            return keyboard
        except Exception as e:
            logger.error(f"Помилка створення меню героїв: {e}")
            return ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="↩️ До навігації")]
                ],
                resize_keyboard=True
            )

    def get_hero_class_menu(self, hero_class: str) -> ReplyKeyboardMarkup:
        """Creates and returns the menu for a specific hero class"""
        try:
            heroes = loc.get_message(f"heroes.classes.{hero_class}.heroes")
            if not heroes:
                raise ValueError(f"Heroes not found for class: {hero_class}")

            # Split heroes into pairs for the keyboard
            hero_pairs = [heroes[i:i + 2] for i in range(0, len(heroes), 2)]
            keyboard_buttons = [[KeyboardButton(text=hero) for hero in pair] for pair in hero_pairs]
            
            # Add back button
            keyboard_buttons.append([
                KeyboardButton(text=loc.get_message("buttons.back_to_hero_classes") or "⬅️ До класів героїв")
            ])

            return ReplyKeyboardMarkup(
                keyboard=keyboard_buttons,
                resize_keyboard=True
            )
        except Exception as e:
            logger.error(f"Помилка створення меню класу героїв {hero_class}: {e}")
            return ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="⬅️ До класів героїв")]
                ],
                resize_keyboard=True
            )


# From base_keyboard.py
# keyboards/base_keyboard.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from typing import List

class BaseKeyboard:
    def __init__(self):
        self._current_level = None

    def create_keyboard(
        self,
        buttons: List[List[str]],
        add_back: bool = True,
        add_main: bool = True
    ) -> ReplyKeyboardMarkup:
        keyboard = []
        
        # Додаємо основні кнопки
        for row in buttons:
            keyboard.append([KeyboardButton(text=str(btn)) for btn in row])
        
        # Додаємо навігаційні кнопки
        nav_row = []
        if add_back and self._current_level != MenuLevel.MAIN:
            nav_row.append(KeyboardButton(text=Buttons.BACK))
        if add_main and self._current_level != MenuLevel.MAIN:
            nav_row.append(KeyboardButton(text=Buttons.MAIN_MENU))
        
        if nav_row:
            keyboard.append(nav_row)
            
        return ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,
            one_time_keyboard=False
        )


# From navigation_keyboard.py
# keyboards/navigation_keyboard.py
from aiogram.types import ReplyKeyboardMarkup
from keyboards.base_keyboard import BaseKeyboard
from keyboards.keyboard_buttons import Buttons

class NavigationKeyboard(BaseKeyboard):
    def get_main_menu(self) -> ReplyKeyboardMarkup:
        buttons = [
            [Buttons.NAVIGATION, Buttons.HEROES],
            [Buttons.PROFILE, Buttons.SETTINGS]
        ]
        return self.create_keyboard(buttons)

    def get_navigation_menu(self) -> ReplyKeyboardMarkup:
        buttons = [
            [Buttons.CHARACTERS, Buttons.MAPS],
            [Buttons.TOURNAMENTS, Buttons.GUIDES],
            [Buttons.MAIN_MENU]
        ]
        return self.create_keyboard(buttons)


# From base.py
# File: keyboards/base_keyboard.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from typing import List

class BaseKeyboard:
    @staticmethod
    def create_keyboard(buttons: List[str], row_width: int = 3) -> ReplyKeyboardMarkup:
        """
        Create a keyboard with specified buttons and row width
        
        Args:
            buttons: List of button texts
            row_width: Number of buttons in each row (default 3)
            
        Returns:
            ReplyKeyboardMarkup with arranged buttons
        """
        keyboard = []
        row = []
        
        for button in buttons:
            row.append(KeyboardButton(text=button))
            if len(row) == row_width:
                keyboard.append(row)
                row = []
                
        if row:  # Add any remaining buttons
            keyboard.append(row)
            
        # Add back button in a separate row
        keyboard.append([KeyboardButton(text="↩️ Назад")])
        
        return ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True
        )


# From main_menu.py
# File: keyboards/main_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from utils.localization import loc

class MainMenu:
    def __init__(self):
        self.builder = ReplyKeyboardBuilder()

    def get_main_menu(self) -> ReplyKeyboardMarkup:
        """Create and return the main menu keyboard"""
        try:
            self.builder.row(
                KeyboardButton(text=loc.get_message("buttons.navigation")),
                KeyboardButton(text=loc.get_message("buttons.characters"))
            )
            
            return self.builder.as_markup(
                resize_keyboard=True,
                one_time_keyboard=False
            )
        except Exception as e:
            logger.error(f"Error creating main menu: {str(e)}")
            # Return a basic fallback keyboard if localization fails
            return ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text="📱 Навігація"),
                        KeyboardButton(text="👥 Герої")
                    ]
                ],
                resize_keyboard=True
            )


# From settings.py
# File: keyboards/settings.py

from .base import BaseKeyboard
from aiogram.types import ReplyKeyboardMarkup

class SettingsKeyboard(BaseKeyboard):
    @classmethod
    def main_menu(cls) -> ReplyKeyboardMarkup:
        """Settings main menu"""
        buttons = [
            "buttons.settings.notifications",
            "buttons.settings.language",
            "buttons.settings.mode",
            "buttons.settings.interface",
            "buttons.settings.privacy",
            "buttons.settings.about"
        ]
        return cls.create_keyboard(buttons, row_width=3)


# From hero_menu.py
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)

class HeroMenu:
    """
    Клас для створення меню класів героїв та списку героїв
    """
    def get_hero_classes_menu(self) -> ReplyKeyboardMarkup:
        try:
            classes = loc.get_message("heroes.classes")
            buttons = [
                KeyboardButton(text=class_info["name"]) for class_info in classes.values()
            ]
            # Розподіляємо кнопки по рядках
            keyboard = []
            for i in range(0, len(buttons), 2):
                keyboard.append(buttons[i:i+2])

            return ReplyKeyboardMarkup(
                keyboard=keyboard,
                resize_keyboard=True,
                one_time_keyboard=True
            )
        except Exception as e:
            logger.error(f"Помилка створення меню класів героїв: {e}")
            return ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=loc.get_message("buttons.menu"))]],
                resize_keyboard=True
            )

    def get_heroes_by_class(self, hero_class: str) -> ReplyKeyboardMarkup:
        try:
            heroes = loc.get_message(f"heroes.classes.{hero_class}.heroes")
            buttons = [KeyboardButton(text=hero) for hero in heroes]
            # Розподіляємо кнопки по рядках
            keyboard = []
            for i in range(0, len(buttons), 2):
                keyboard.append(buttons[i:i+2])

            # Додаємо кнопку "Назад"
            keyboard.append([KeyboardButton(text=loc.get_message("buttons.back_to_hero_classes"))])

            return ReplyKeyboardMarkup(
                keyboard=keyboard,
                resize_keyboard=True,
                one_time_keyboard=True
            )
        except Exception as e:
            logger.error(f"Помилка створення меню героїв для класу {hero_class}: {e}")
            return ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=loc.get_message("buttons.menu"))]],
                resize_keyboard=True
            )


# From keyboard_buttons.py
from enum import Enum, auto

class MenuLevel(Enum):
    MAIN = auto()
    NAVIGATION = auto()
    HEROES = auto()
    TOURNAMENTS = auto()
    PROFILE = auto()
    SETTINGS = auto()

class Buttons(str, Enum):
    # Головне меню (MAIN)
    NAVIGATION = "🧭 Навігація"
    HEROES = "🎯 Герої"
    TOURNAMENTS = "🏆 Турніри"
    PROFILE = "👤 Профіль"
    SETTINGS = "⚙️ Налаштування"
    
    # Меню навігації (NAVIGATION)
    CHARACTERS = "👥 Персонажі"
    MAPS = "🗺 Мапи"
    GUIDES = "📖 Гайди"
    
    # Навігаційні кнопки
    BACK = "🔙 Назад"
    MAIN_MENU = "🏠 Головне меню"


# From profile_keyboard.py
# File: keyboards/profile_keyboard.py
from .base_keyboard import BaseKeyboard

class ProfileKeyboard(BaseKeyboard):
    def get_profile_menu(self) -> ReplyKeyboardMarkup:
        buttons = [
            "📊 Статистика",
            "🏆 Досягнення",
            "⚙️ Налаштування",
            "📝 Зворотний зв'язок",
            "❓ Допомога",
            "🔙 Назад до Головного меню"
        ]
        return self.create_markup(buttons, row_width=2)

    # Add other profile submenus...


# From main_keyboard.py
# keyboards/main_keyboard.py
from aiogram.types import ReplyKeyboardMarkup
from keyboards.base_keyboard import BaseKeyboard

class MainKeyboard(BaseKeyboard):
    """Class for main keyboard functionalities"""

    def get_main_menu(self) -> ReplyKeyboardMarkup:
        keyboard = [
            ["🧭 Навігація", "🎯 Герої"],
            ["🪪 Профіль", "⚙️ Налаштування"],
            ["🎫 Купити білети", "📊 Статистика"]
        ]
        return self.create_reply_markup(keyboard)

    def get_navigation_menu(self) -> ReplyKeyboardMarkup:
        keyboard = [
            ["👥 Персонажі", "🗺 Мапи"],
            ["🏆 Турніри", "📖 Гайди"],
            ["🔙 Назад до Головного меню"]
        ]
        return self.create_reply_markup(keyboard)

    # Інші методи...


# From profile_menu.py
# File: keyboards/profile_menu.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from utils.localization import loc
import logging

logger = logging.getLogger(__name__)

class ProfileMenu:
    def get_profile_menu(self) -> ReplyKeyboardMarkup:
        """
        Creates and returns the profile menu keyboard markup.
        Returns a simplified fallback keyboard if there's an error.
        """
        try:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=loc.get_message("buttons.statistics") or "📊 Статистика"),
                        KeyboardButton(text=loc.get_message("buttons.achievements") or "🏆 Досягнення")
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.settings") or "⚙️ Налаштування"),
                        KeyboardButton(text=loc.get_message("buttons.feedback") or "📝 Зворотній зв'язок")
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.back") or "↩️ Назад")
                    ]
                ],
                resize_keyboard=True
            )
            return keyboard
        except Exception as e:
            logger.error(f"Помилка створення профільного меню: {e}")
            # Fallback keyboard with just the back button
            return ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="↩️ Назад")]
                ],
                resize_keyboard=True
            )

    def get_statistics_menu(self) -> ReplyKeyboardMarkup:
        """
        Creates and returns the statistics submenu keyboard markup.
        """
        try:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=loc.get_message("buttons.personal_stats") or "👤 Особиста статистика"),
                        KeyboardButton(text=loc.get_message("buttons.global_stats") or "🌐 Загальна статистика")
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.back") or "↩️ Назад")
                    ]
                ],
                resize_keyboard=True
            )
            return keyboard
        except Exception as e:
            logger.error(f"Помилка створення меню статистики: {e}")
            return ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="↩️ Назад")]
                ],
                resize_keyboard=True
            )

    def get_achievements_menu(self) -> ReplyKeyboardMarkup:
        """
        Creates and returns the achievements submenu keyboard markup.
        """
        try:
            keyboard = ReplyKeyboardMarkup(
                keyboard=[
                    [
                        KeyboardButton(text=loc.get_message("buttons.my_achievements") or "🏆 Мої досягнення"),
                        KeyboardButton(text=loc.get_message("buttons.leaderboard") or "🏅 Рейтинг")
                    ],
                    [
                        KeyboardButton(text=loc.get_message("buttons.back") or "↩️ Назад")
                    ]
                ],
                resize_keyboard=True
            )
            return keyboard
        except Exception as e:
            logger.error(f"Помилка створення меню досягнень: {e}")
            return ReplyKeyboardMarkup(
                keyboard=[
                    [KeyboardButton(text="↩️ Назад")]
                ],
                resize_keyboard=True
            )


# From menu_keyboard.py
from .base_keyboard import BaseKeyboard
from .keyboard_buttons import Buttons, MenuLevel

class MenuKeyboard(BaseKeyboard):
    def __init__(self):
        super().__init__()
        self._current_level = MenuLevel.MAIN

    def get_main_menu(self):
        self._current_level = MenuLevel.MAIN
        buttons = [
            [Buttons.NAVIGATION.value, Buttons.HEROES.value],
            [Buttons.TOURNAMENTS.value, Buttons.PROFILE.value],
            [Buttons.SETTINGS.value]
        ]
        return self.create_keyboard(buttons, add_back=False, add_main=False)

    def get_navigation_menu(self):
        self._current_level = MenuLevel.NAVIGATION
        buttons = [
            [Buttons.CHARACTERS.value, Buttons.MAPS.value],
            [Buttons.GUIDES.value]
        ]
        return self.create_keyboard(buttons)

    def get_heroes_menu(self):
        self._current_level = MenuLevel.HEROES
        buttons = [
            [Buttons.TANK.value, Buttons.FIGHTER.value],
            [Buttons.ASSASSIN.value, Buttons.MAGE.value],
            [Buttons.MARKSMAN.value, Buttons.SUPPORT.value]
        ]
        return self.create_keyboard(buttons)

    def get_tournaments_menu(self):
        self._current_level = MenuLevel.TOURNAMENTS
        buttons = [
            [Buttons.ACTIVE.value, Buttons.UPCOMING.value],
            [Buttons.PAST.value, Buttons.CREATE.value]
        ]
        return self.create_keyboard(buttons)

    def get_profile_menu(self):
        self._current_level = MenuLevel.PROFILE
        buttons = [
            [Buttons.STATS.value, Buttons.ACHIEVEMENTS.value],
            [Buttons.INVENTORY.value]
        ]
        return self.create_keyboard(buttons)

    def get_settings_menu(self):
        self._current_level = MenuLevel.SETTINGS
        buttons = [
            ["Мова", "Сповіщення"],
            ["Тема", "Приватність"]
        ]
        return self.create_keyboard(buttons)



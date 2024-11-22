# Імпорти доступних меню
from .achievements_menu import get_achievements_menu
from .builds_menu import get_builds_menu
from .hero_menu import get_hero_menu
from .main_menu import get_main_menu
from .navigation_menu import get_navigation_menu
from .profile_menu import get_profile_menu
from .settings_menu import get_settings_menu
from .statistics_menu import get_statistics_menu
from .voting_menu import get_voting_menu

# Заглушка для функцій, які ще не реалізовані
def get_counter_picks_menu():
    return None  # Тимчасова заглушка

# Визначаємо, які функції можна імпортувати за допомогою `from keyboards import *`
__all__ = [
    "get_achievements_menu",
    "get_builds_menu",
    "get_hero_menu",
    "get_main_menu",
    "get_navigation_menu",
    "get_profile_menu",
    "get_settings_menu",
    "get_statistics_menu",
    "get_voting_menu",
]

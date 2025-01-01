# keyboards/menus/main_menu.py

from aiogram.types import ReplyKeyboardMarkup
from ..factories import create_menu
from texts.enums import MenuButton  # Оновлено імпорт з texts

def get_main_menu() -> ReplyKeyboardMarkup:
    """
    Генерує клавіатуру для головного меню з кнопками "Навігація" та "Профіль".
    """
    return create_menu(
        buttons=[MenuButton.NAVIGATION, MenuButton.PROFILE],
        placeholder="Оберіть одну з основних опцій",
        row_width=2
    )

# texts/__init__.py

from .enums import MenuButton, LanguageButton
from .messages_intro import (
    WELCOME_NEW_USER_TEXT,
    INTRO_PAGE_1_TEXT,
    INTRO_PAGE_2_TEXT,
    INTRO_PAGE_3_TEXT,
    WELCOME_NEW_USER_TEXT,
    # Додайте інші текстові константи
)
from .messages_main_menu import (
    MAIN_MENU_TEXT,
    MAIN_MENU_DESCRIPTION,
    MAIN_MENU_ERROR_TEXT,
    # Додайте інші текстові константи
)
from .messages_profile import (
    PROFILE_MENU_TEXT,
    PROFILE_INTERACTIVE_TEXT,
    VIEW_PROFILE_TEXT,
    EDIT_PROFILE_TEXT,
    # Додайте інші текстові константи
)
# Імпортуйте інші текстові модулі аналогічно

__all__ = [
    "MenuButton",
    "LanguageButton",
    "WELCOME_NEW_USER_TEXT",
    "INTRO_PAGE_1_TEXT",
    "INTRO_PAGE_2_TEXT",
    "INTRO_PAGE_3_TEXT",
    "MAIN_MENU_TEXT",
    "MAIN_MENU_DESCRIPTION",
    "MAIN_MENU_ERROR_TEXT",
    "PROFILE_MENU_TEXT",
    "PROFILE_INTERACTIVE_TEXT",
    "VIEW_PROFILE_TEXT",
    "EDIT_PROFILE_TEXT",
    # Додайте інші текстові константи
]

# keyboards/intro.py
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_intro_keyboard(page: int) -> InlineKeyboardMarkup:
    """
    Get intro navigation keyboard
    
    Args:
        page: Current page number
        
    Returns:
        InlineKeyboardMarkup: Navigation keyboard
    """
    keyboard = []
    
    # Navigation row
    nav_row = []
    
    if page > 1:
        nav_row.append(
            InlineKeyboardButton(
                text="⬅️ Назад",
                callback_data="intro_prev"
            )
        )
        
    if page < 3:  # Assuming we have 3 intro pages
        nav_row.append(
            InlineKeyboardButton(
                text="Далі ➡️",
                callback_data="intro_next"
            )
        )
    
    if page == 3:
        nav_row.append(
            InlineKeyboardButton(
                text="✅ Завершити",
                callback_data="intro_complete"
            )
        )
    
    keyboard.append(nav_row)
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

# keyboards/__init__.py
from .intro import get_intro_keyboard

__all__ = ['get_intro_keyboard']

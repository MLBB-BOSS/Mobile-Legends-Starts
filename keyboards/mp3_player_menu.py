# keyboards/mp3_player_menu.py
# UTC:23:51
# 2024-11-25
# Author: MLBB-BOSS
# Description: MP3 Player menu keyboard layouts
# The era of artificial intelligence.

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_mp3_player_keyboard() -> ReplyKeyboardMarkup:
    """Меню MP3 плеєра"""
    buttons = [
        [
            KeyboardButton(text="▶️ Відтворити"),
            KeyboardButton(text="⏸️ Пауза"),
            KeyboardButton(text="⏹️ Стоп")
        ],
        [
            KeyboardButton(text="⏭️ Наступний трек"),
            KeyboardButton(text="⏮️ Попередній трек")
        ],
        [KeyboardButton(text="◀️ Назад до Навігації")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)


from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from enum import Enum

class MenuButton(Enum):
    NAVIGATION = "🧭 Навігація"
    PROFILE = "🪪 Профіль"
    META = "🔥 META"
    M6 = "🏆 M6"
    GPT = "👾 GPT"
    BACK = "🔙 Назад"
    BACK_TO_MAIN_MENU = "🔙 Меню"
    HEROES = "🥷 Персонажі"
    GUIDES = "📚 Гайди"
    COUNTER_PICKS = "⚖️ Контр-піки"
    BUILDS = "🛡️ Білди"
    VOTING = "📊 Голосування"
    NEW_GUIDES = "🆕 Нові Гайди"
    POPULAR_GUIDES = "🌟 Топ Гайди"
    BEGINNER_GUIDES = "📘 Новачкам"
    ADVANCED_TECHNIQUES = "🧙 Стратегії гри"
    TEAMPLAY_GUIDES = "🤝 Командна Гра"
    TANK = "🛡️ Танки"
    MAGE = "🧙‍♂️ Маги"
    MARKSMAN = "🏹 Стрільці"
    ASSASSIN = "⚔️ Асасіни"
    SUPPORT = "❤️ Сапорти"
    FIGHTER = "🗡️ Бійці"
    COMPARISON = "⚖️ Порівняти"
    SEARCH_HERO = "🔎 Шукати"
    HELP = "❓ Допомога"
    ANALYTICS = "📈 Дані"
    STATISTICS = "📊 Статистика"
    TOURNAMENTS = "🏆 Турніри"
    BUILDS_OVERVIEW = "🛠️ Білди Огляд"
    META_OVERVIEW = "🔥 META Огляд"

menu_button_to_class = {
    MenuButton.TANK.value: "Танк",
    MenuButton.MAGE.value: "Маг",
    MenuButton.MARKSMAN.value: "Стрілець",
    MenuButton.ASSASSIN.value: "Асасін",
    MenuButton.SUPPORT.value: "Підтримка",
    MenuButton.FIGHTER.value: "Боєць",
    MenuButton.HELP.value: "Допомога",
    MenuButton.ANALYTICS.value: "Аналітика",
    MenuButton.STATISTICS.value: "Статистика",
    MenuButton.TOURNAMENTS.value: "Турніри",
    MenuButton.BUILDS_OVERVIEW.value: "Білди",
    MenuButton.META_OVERVIEW.value: "META",
}

def create_menu(buttons, row_width=3):
    keyboard_buttons = [
        KeyboardButton(text=button.value if isinstance(button, MenuButton) else button) for button in buttons
    ]
    keyboard = [
        keyboard_buttons[i:i + row_width]
        for i in range(0, len(keyboard_buttons), row_width)
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

def get_tournament_menu():
    return create_menu(
        [
            MenuButton.TOURNAMENTS,
            MenuButton.ANALYTICS,
            MenuButton.STATISTICS,
            MenuButton.BACK_TO_MAIN_MENU,
        ],
        row_width=3
    )

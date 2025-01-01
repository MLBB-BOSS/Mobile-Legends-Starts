# texts/data.py

from typing import Dict, List
from .enums import MenuButton

# Мапінг кнопок меню до класів героїв.
MENU_BUTTON_TO_CLASS: Dict[str, str] = {
    MenuButton.CREATE_TOURNAMENT.value: "Створити Турнір",
    MenuButton.VIEW_TOURNAMENTS.value: "Переглянути Турніри",
    MenuButton.M6_INFO.value: "Інформація про M6",
    MenuButton.M6_STATS.value: "Статистика M6",
    MenuButton.M6_NEWS.value: "Новини M6",
    MenuButton.META.value: "META Інформація",
    MenuButton.COMPARISON.value: "Порівняння Героїв",
    MenuButton.VOTING.value: "Голосування",
    MenuButton.SEARCH_HERO.value: "Пошук Героя",
    MenuButton.COUNTER_SEARCH.value: "Пошук Контр-Піка",
    MenuButton.COUNTER_LIST.value: "Список Контр-Піків",
    MenuButton.CREATE_TEAM.value: "Створити Команду",
    MenuButton.VIEW_TEAMS.value: "Переглянути Команди",
    MenuButton.CREATE_TRADE.value: "Створити Торгівлю",
    MenuButton.VIEW_TRADES.value: "Переглянути Торгівлі",
    MenuButton.MANAGE_TRADES.value: "Управління Торгівлями",
    MenuButton.GPT_DATA_GENERATION.value: "Генерація Даних GPT",
    MenuButton.GPT_HINTS.value: "Поради GPT",
    MenuButton.GPT_HERO_STATS.value: "Статистика Героя GPT",
    "Танк": "Танк",
    "Маг": "Маг",
    "Стрілець": "Стрілець",
    "Асасін": "Асасін",
    "Підтримка": "Підтримка",
    "Боєць": "Боєць"
}

# Інформація про героїв, згрупованих за класами.
heroes_by_class: Dict[str, List[Dict[str, str]]] = {
    "Танк": [
        {"name": "Танк Герой 1", "description": "Опис Танк Героя 1."},
        {"name": "Танк Герой 2", "description": "Опис Танк Героя 2."},
    ],
    "Маг": [
        {"name": "Маг Герой 1", "description": "Опис Маг Героя 1."},
        {"name": "Маг Герой 2", "description": "Опис Маг Героя 2."},
    ],
    "Стрілець": [
        {"name": "Стрілець Герой 1", "description": "Опис Стрілець Героя 1."},
        {"name": "Стрілець Герой 2", "description": "Опис Стрілець Героя 2."},
    ],
    "Асасін": [
        {"name": "Асасін Герой 1", "description": "Опис Асасін Героя 1."},
        {"name": "Асасін Герой 2", "description": "Опис Асасін Героя 2."},
    ],
    "Підтримка": [
        {"name": "Підтримка Герой 1", "description": "Опис Підтримки Героя 1."},
        {"name": "Підтримка Герой 2", "description": "Опис Підтримки Героя 2."},
    ],
    "Боєць": [
        {"name": "Боєць Герой 1", "description": "Опис Боєць Героя 1."},
        {"name": "Боєць Герой 2", "description": "Опис Боєць Героя 2."},
    ],
}

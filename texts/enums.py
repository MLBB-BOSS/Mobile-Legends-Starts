# texts/enums.py

from enum import Enum

class MenuButton(Enum):
    CREATE_TOURNAMENT = "Створити Турнір"
    VIEW_TOURNAMENTS = "Переглянути Турніри"
    M6_INFO = "Інформація про M6"
    M6_STATS = "Статистика M6"
    M6_NEWS = "Новини M6"
    META = "META Інформація"
    COMPARISON = "Порівняння Героїв"
    VOTING = "Голосування"
    SEARCH_HERO = "Пошук Героя"
    COUNTER_SEARCH = "Пошук Контр-Піка"
    COUNTER_LIST = "Список Контр-Піків"
    CREATE_TEAM = "Створити Команду"
    VIEW_TEAMS = "Переглянути Команди"
    CREATE_TRADE = "Створити Торгівлю"
    VIEW_TRADES = "Переглянути Торгівлі"
    MANAGE_TRADES = "Управління Торгівлями"
    GPT_DATA_GENERATION = "Генерація Даних GPT"
    GPT_HINTS = "Поради GPT"
    GPT_HERO_STATS = "Статистика Героя GPT"

class LanguageButton(Enum):
    UKRAINIAN = "🇺🇦 Українська"
    ENGLISH = "🇬🇧 Англійська"
    BACK = "🔙 Назад"

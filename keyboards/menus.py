# keyboards/menus.py

from enum import Enum

class MenuButton(Enum):
    # Головне Меню
    NAVIGATION = "🧭 Навігація"
    PROFILE = "🪪 Профіль"
    META = "🔥 META"
    M6 = "🏆 M6"
    GPT = "👾 GPT"

    # Меню Навігації
    CHARACTERS = "🥷 Персонажі"
    GUIDES = "📚 Гайди"
    COUNTER_PICKS = "⚖️ Контр-піки"
    BUILDS = "🛡️ Білди"
    VOTING = "📊 Голосування"

    # Меню Гайди
    NEW_GUIDES = "🆕 Нові Гайди"
    TOP_GUIDES = "🌟 Топ Гайди"
    BEGINNER_GUIDES = "📘 Новачкам"
    ADVANCED_TECHNIQUES = "🧙 Стратегії гри"
    TEAMPLAY_GUIDES = "🤝 Командна Гра"

    # Меню Контр-піки
    COUNTER_SEARCH = "🔎 Пошук Контр-піку"
    COUNTER_LIST = "📝 Список Персонажів"

    # Меню Білди
    CREATE_BUILD = "🏗️ Створити Білд"
    MY_BUILDS = "📄 Збережені Білди"
    POPULAR_BUILDS = "🔥 Популярні Білди"

    # Меню Голосування
    CURRENT_VOTES = "📍 Поточні Опитування"
    MY_VOTES = "📋 Мої Голосування"
    SUGGEST_TOPIC = "➕ Запропонувати Тему"

    # Меню Профіль
    STATISTICS = "📈 Статистика"
    ACHIEVEMENTS = "🏆 Досягнення"
    SETTINGS = "⚙️ Налаштування"
    FEEDBACK = "💌 Зворотний Зв’язок"
    HELP = "❓ Допомога"

    # Меню Статистика
    ACTIVITY = "📊 Загальна Активність"
    RANKING = "🥇 Рейтинг"
    GAME_STATS = "🎮 Ігрова Статистика"

    # Меню Досягнення
    BADGES = "🎖️ Мої Бейджі"
    PROGRESS = "🚀 Прогрес"
    TOURNAMENT_STATS = "🏅 Турнірна Статистика"
    AWARDS = "🎟️ Отримані Нагороди"

    # Меню Налаштування
    LANGUAGE = "🌐 Мова Інтерфейсу"
    CHANGE_USERNAME = "ℹ️ Змінити Username"
    UPDATE_ID = "🆔 Оновити ID"
    NOTIFICATIONS = "🔔 Сповіщення"

    # Інші кнопки
    BACK = "🔙 Назад"
    BACK_TO_MAIN_MENU = "🔙 Меню"
    HEROES = "🦸‍♂️ Герої"
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from enum import Enum
import logging

# Налаштування логування
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class MenuButton(Enum):
    # Головне Меню
    NAVIGATION = "🧭 Навігація"
    PROFILE = "🪪 Мій Профіль"

    # Розділ Навігація
    HEROES = "🥷 Персонажі"
    BUILDS = "🛡️ Білди"
    COUNTER_PICKS = "⚖️ Контр-піки"
    GUIDES = "📚 Гайди"
    VOTING = "📊 Голосування"
    M6 = "🏆 M6"
    GPT = "👾 GPT"
    META = "🔥 META"
    TOURNAMENTS = "🏆 Турніри"
    BACK_NAVIGATION = "🔙 Назад"

    # Розділ Персонажі
    TANK = "🛡️ Танк"
    MAGE = "🧙‍♂️ Маг"
    MARKSMAN = "🏹 Стрілець"
    ASSASSIN = "⚔️ Асасін"
    SUPPORT = "❤️ Підтримка"
    FIGHTER = "🗡️ Боєць"
    COMPARISON = "⚖️ Порівняння"
    SEARCH_HERO = "🔎 Пошук"
    BACK_HEROES = "🔙 Назад"

    # Розділ Гайди
    NEW_GUIDES = "🆕 Нові Гайди"
    TOP_GUIDES = "🌟 Топ Гайди"
    BEGINNER_GUIDES = "📘 Для Початківців"
    GAME_STRATEGIES = "🧙 Стратегії гри"
    TEAMPLAY_GUIDES = "🤝 Командна Гра"
    BACK_GUIDES = "🔙 Назад"

    # Розділ Контр-піки
    COUNTER_SEARCH = "🔎 Пошук"
    COUNTER_LIST = "📝 Список Персонажів"
    BACK_COUNTER_PICKS = "🔙 Назад"

    # Розділ Білди
    CREATE_BUILD = "🏗️ Створити"
    MY_BUILDS = "📄 Обрані"
    POPULAR_BUILDS = "🔥 Популярні"
    BACK_BUILDS = "🔙 Назад"

    # Розділ Голосування
    CURRENT_VOTES = "📍 Поточні Опитування"
    MY_VOTES = "📋 Мої Голосування"
    SUGGEST_TOPIC = "➕ Запропонувати Тему"
    BACK_VOTING = "🔙 Назад"

    # Розділ M6
    TOURNAMENT_INFO = "🏆 Турнірна Інформація"
    M6_STATS = "📈 Статистика M6"
    M6_NEWS = "📰 Новини M6"
    BACK_M6 = "🔙 Назад"

    # Розділ GPT
    GPT_DATA_GENERATION = "🤖 Генерація Даних"
    GPT_HINTS = "📝 Підказки"
    GPT_HERO_STATS = "📊 Статистика Героїв"
    BACK_GPT = "🔙 Назад"

    # Розділ META
    META_HERO_LIST = "📋 Список Героїв у Мету"
    META_RECOMMENDATIONS = "🌟 Рекомендації"
    META_UPDATES = "🔄 Оновлення Мети"
    BACK_META = "🔙 Назад"

    # Розділ Турніри
    CREATE_TOURNAMENT = "🆕 Створити Турнір"
    VIEW_TOURNAMENTS = "📋 Переглянути Турніри"
    BACK_TOURNAMENTS = "🔙 Назад"

    # Розділ Профіль
    STATISTICS = "📈 Статистика"
    ACHIEVEMENTS = "🏆 Досягнення"
    SETTINGS = "⚙️ Налаштування"
    FEEDBACK = "💌 Зворотний Зв'язок"
    HELP = "❓ Допомога"
    BACK_PROFILE = "🔙 Назад до Головного Меню"

    # Підрозділ Статистика
    OVERALL_ACTIVITY = "📊 Загальна Активність"
    USER_RANKING = "🥇 Рейтинг"
    DETAILED_GAME_STATS = "🎮 Ігрова Статистика"
    BACK_STATISTICS = "🔙 Назад"

    # Підрозділ Досягнення
    MY_BADGES = "🎖️ Мої Бейджі"
    MY_PROGRESS = "🚀 Прогрес"
    MY_TOURNAMENT_STATS = "🏅 Турнірна Статистика"
    MY_AWARDS = "🎟️ Отримані Нагороди"
    BACK_ACHIEVEMENTS = "🔙 Назад"

    # Підрозділ Налаштування
    INTERFACE_LANGUAGE = "🌐 Мова Інтерфейсу"
    CHANGE_GAME_USERNAME = "ℹ️ Змінити Username"
    UPDATE_GAME_ID = "🆔 Оновити ID"
    CONFIGURE_NOTIFICATIONS = "🔔 Сповіщення"
    BACK_SETTINGS = "🔙 Назад"

    # Підрозділ Зворотного Зв'язку
    SEND_USER_FEEDBACK = "✏️ Надіслати Відгук"
    REPORT_USER_BUG = "🐛 Повідомити про Помилку"
    BACK_FEEDBACK = "🔙 Назад"

    # Підрозділ Допомоги
    USER_INSTRUCTIONS = "📄 Інструкції"
    USER_FAQ = "❔ FAQ"
    USER_HELP_SUPPORT = "📞 Підтримка"
    BACK_HELP = "🔙 Назад"

# Відповідність кнопок класам героїв
menu_button_to_class = {
    MenuButton.TANK.value: "Танк",
    MenuButton.MAGE.value: "Маг",
    MenuButton.MARKSMAN.value: "Стрілець",
    MenuButton.ASSASSIN.value: "Асасін",
    MenuButton.SUPPORT.value: "Підтримка",
    MenuButton.FIGHTER.value: "Боєць",
}

# Повний список героїв за класами
heroes_by_class = {
    "Танк": [
        "Alice", "Tigreal", "Akai", "Franco", "Minotaur", "Lolia", "Gatotkaca", "Grock",
        "Hylos", "Uranus", "Belerick", "Khufra", "Esmeralda", "Terizla", "Baxia", "Masha",
        "Atlas", "Barats", "Edith", "Fredrinn", "Johnson", "Hilda", "Carmilla", "Gloo", "Chip"
    ],
    "Маг": [
        "Vale", "Lunox", "Kadita", "Cecillion", "Luo Yi", "Xavier", "Novaria", "Zhuxin", "Harley",
        "Yve", "Aurora", "Faramis", "Esmeralda", "Kagura", "Cyclops", "Vexana", "Odette", "Zhask"
    ],
    "Стрілець": [
        "Popol and Kupa", "Brody", "Beatrix", "Natan", "Melissa", "Ixia", "Hanabi", "Claude",
        "Kimmy", "Granger", "Wanwan", "Miya", "Bruno", "Clint", "Layla", "Yi Sun-shin", "Moskov",
        "Roger", "Karrie", "Irithel", "Lesley"
    ],
    "Асасін": [
        "Saber", "Alucard", "Zilong", "Fanny", "Natalia", "Yi Sun-shin", "Lancelot", "Helcurt",
        "Lesley", "Selena", "Mathilda", "Paquito", "Yin", "Arlott", "Harley", "Suyou"
    ],
    "Підтримка": [
        "Rafaela", "Minotaur", "Lolita", "Estes", "Angela", "Faramis", "Mathilda", "Florin", "Johnson"
    ],
    "Боєць": [
        "Balmond", "Alucard", "Bane", "Zilong", "Freya", "Alpha", "Ruby", "Roger",
        "Gatotkaca", "Jawhead", "Martis", "Aldous", "Minsitthar", "Terizla", "X.Borg",
        "Dyroth", "Masha", "Silvanna", "Yu Zhong", "Khaleed", "Barats", "Paquito",
        "Phoveus", "Aulus", "Fiddrin", "Arlott", "Cici", "Kaja", "Leomord", "Thamuz",
        "Badang", "Guinevere"
    ],
}

def create_menu(buttons, row_width=2):
    """
    Створює клавіатуру з кнопками.
    :param buttons: Список кнопок (MenuButton або str).
    :param row_width: Кількість кнопок у рядку.
    :return: ReplyKeyboardMarkup
    """
    if not all(isinstance(button, MenuButton) or isinstance(button, str) for button in buttons):
        raise ValueError("Усі елементи у списку кнопок повинні бути екземплярами MenuButton або str.")
    logger.info(f"Створення меню з кнопками: {[button.value if isinstance(button, MenuButton) else button for button in buttons]}")
    keyboard_buttons = [
        KeyboardButton(text=button.value if isinstance(button, MenuButton) else button) for button in buttons
    ]
    keyboard = [
        keyboard_buttons[i:i + row_width]
        for i in range(0, len(keyboard_buttons), row_width)
    ]
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# Функції для створення кожного меню

# 1. Головне меню
def get_main_menu():
    return create_menu(
        [
            MenuButton.NAVIGATION,
            MenuButton.PROFILE
        ],
        row_width=2
    )

# 2. Навігація
def get_navigation_menu():
    return create_menu(
        [
            MenuButton.HEROES,
            MenuButton.BUILDS,
            MenuButton.COUNTER_PICKS,
            MenuButton.GUIDES,
            MenuButton.VOTING,
            MenuButton.M6,
            MenuButton.GPT,
            MenuButton.META,
            MenuButton.TOURNAMENTS,
            MenuButton.BACK_NAVIGATION
        ],
        row_width=3
    )

# 3. Персонажі
def get_heroes_menu():
    return create_menu(
        [
            MenuButton.TANK,
            MenuButton.MAGE,
            MenuButton.MARKSMAN,
            MenuButton.ASSASSIN,
            MenuButton.SUPPORT,
            MenuButton.FIGHTER,
            MenuButton.COMPARISON,
            MenuButton.SEARCH_HERO,
            MenuButton.BACK_HEROES
        ],
        row_width=3
    )

# 4. Меню класу героїв (Танк, Маг, Стрілець, Асасін, Підтримка, Боєць)
def get_hero_class_menu(hero_class):
    heroes = heroes_by_class.get(hero_class, [])
    buttons = [KeyboardButton(text=hero) for hero in heroes]
    row_width = 3
    keyboard = [buttons[i:i+row_width] for i in range(0, len(buttons), row_width)]
    keyboard.append([KeyboardButton(text=MenuButton.BACK_HEROES.value)])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)

# 5. Білди
def get_builds_menu():
    return create_menu(
        [
            MenuButton.CREATE_BUILD,
            MenuButton.MY_BUILDS,
            MenuButton.POPULAR_BUILDS,
            MenuButton.BACK_BUILDS
        ],
        row_width=2
    )

# 6. Контр-піки
def get_counter_picks_menu():
    return create_menu(
        [
            MenuButton.COUNTER_SEARCH,
            MenuButton.COUNTER_LIST,
            MenuButton.BACK_COUNTER_PICKS
        ],
        row_width=2
    )

# 7. Гайди
def get_guides_menu():
    return create_menu(
        [
            MenuButton.NEW_GUIDES,
            MenuButton.TOP_GUIDES,
            MenuButton.BEGINNER_GUIDES,
            MenuButton.GAME_STRATEGIES,
            MenuButton.TEAMPLAY_GUIDES,
            MenuButton.BACK_GUIDES
        ],
        row_width=2
    )

# 8. Голосування
def get_voting_menu():
    return create_menu(
        [
            MenuButton.CURRENT_VOTES,
            MenuButton.MY_VOTES,
            MenuButton.SUGGEST_TOPIC,
            MenuButton.BACK_VOTING
        ],
        row_width=2
    )

# 9. M6
def get_m6_menu():
    return create_menu(
        [
            MenuButton.TOURNAMENT_INFO,
            MenuButton.M6_STATS,
            MenuButton.M6_NEWS,
            MenuButton.BACK_M6
        ],
        row_width=2
    )

# 10. GPT
def get_gpt_menu():
    return create_menu(
        [
            MenuButton.GPT_DATA_GENERATION,
            MenuButton.GPT_HINTS,
            MenuButton.GPT_HERO_STATS,
            MenuButton.BACK_GPT
        ],
        row_width=2
    )

# 11. META
def get_meta_menu():
    return create_menu(
        [
            MenuButton.META_HERO_LIST,
            MenuButton.META_RECOMMENDATIONS,
            MenuButton.META_UPDATES,
            MenuButton.BACK_META
        ],
        row_width=2
    )

# 12. Турніри
def get_tournaments_menu():
    return create_menu(
        [
            MenuButton.CREATE_TOURNAMENT,
            MenuButton.VIEW_TOURNAMENTS,
            MenuButton.BACK_TOURNAMENTS
        ],
        row_width=2
    )

# 13. Профіль
def get_profile_menu():
    return create_menu(
        [
            MenuButton.STATISTICS,
            MenuButton.ACHIEVEMENTS,
            MenuButton.SETTINGS,
            MenuButton.FEEDBACK,
            MenuButton.HELP,
            MenuButton.BACK_PROFILE
        ],
        row_width=3
    )

# 14. Статистика
def get_statistics_menu():
    return create_menu(
        [
            MenuButton.OVERALL_ACTIVITY,
            MenuButton.USER_RANKING,
            MenuButton.DETAILED_GAME_STATS,
            MenuButton.BACK_STATISTICS
        ],
        row_width=2
    )

# 15. Досягнення
def get_achievements_menu():
    return create_menu(
        [
            MenuButton.MY_BADGES,
            MenuButton.MY_PROGRESS,
            MenuButton.MY_TOURNAMENT_STATS,
            MenuButton.MY_AWARDS,
            MenuButton.BACK_ACHIEVEMENTS
        ],
        row_width=2
    )

# 16. Налаштування
def get_settings_menu():
    return create_menu(
        [
            MenuButton.INTERFACE_LANGUAGE,
            MenuButton.CHANGE_GAME_USERNAME,
            MenuButton.UPDATE_GAME_ID,
            MenuButton.CONFIGURE_NOTIFICATIONS,
            MenuButton.BACK_SETTINGS
        ],
        row_width=2
    )

# 17. Зворотний зв'язок
def get_feedback_menu():
    return create_menu(
        [
            MenuButton.SEND_USER_FEEDBACK,
            MenuButton.REPORT_USER_BUG,
            MenuButton.BACK_FEEDBACK
        ],
        row_width=2
    )

# 18. Допомога
def get_help_menu():
    return create_menu(
        [
            MenuButton.USER_INSTRUCTIONS,
            MenuButton.USER_FAQ,
            MenuButton.USER_HELP_SUPPORT,
            MenuButton.BACK_HELP
        ],
        row_width=2
    )

# 19. Підменю Статистики
def get_statistics_submenu():
    return create_menu(
        [
            MenuButton.OVERALL_ACTIVITY,
            MenuButton.USER_RANKING,
            MenuButton.DETAILED_GAME_STATS,
            MenuButton.BACK_STATISTICS
        ],
        row_width=2
    )

# 20. Підменю Досягнень
def get_achievements_submenu():
    return create_menu(
        [
            MenuButton.MY_BADGES,
            MenuButton.MY_PROGRESS,
            MenuButton.MY_TOURNAMENT_STATS,
            MenuButton.MY_AWARDS,
            MenuButton.BACK_ACHIEVEMENTS
        ],
        row_width=2
    )

# 21. Підменю Налаштувань
def get_settings_submenu():
    return create_menu(
        [
            MenuButton.INTERFACE_LANGUAGE,
            MenuButton.CHANGE_GAME_USERNAME,
            MenuButton.UPDATE_GAME_ID,
            MenuButton.CONFIGURE_NOTIFICATIONS,
            MenuButton.BACK_SETTINGS
        ],
        row_width=2
    )

# 22. Підменю Зворотного зв'язку
def get_feedback_submenu():
    return create_menu(
        [
            MenuButton.SEND_USER_FEEDBACK,
            MenuButton.REPORT_USER_BUG,
            MenuButton.BACK_FEEDBACK
        ],
        row_width=2
    )

# 23. Підменю Допомоги
def get_help_submenu():
    return create_menu(
        [
            MenuButton.USER_INSTRUCTIONS,
            MenuButton.USER_FAQ,
            MenuButton.USER_HELP_SUPPORT,
            MenuButton.BACK_HELP
        ],
        row_width=2
    )

# 24. Створення Турніру
def get_create_tournament_menu():
    return create_menu(
        [
            MenuButton.TOURNAMENT_INFO,
            MenuButton.M6_STATS,
            MenuButton.M6_NEWS,
            MenuButton.BACK_TOURNAMENTS
        ],
        row_width=2
    )

# 25. Перегляд Турнірів
def get_view_tournaments_menu():
    return create_menu(
        [
            MenuButton.TOURNAMENT_INFO,
            MenuButton.M6_STATS,
            MenuButton.M6_NEWS,
            MenuButton.BACK_TOURNAMENTS
        ],
        row_width=2
    )

# 26. Додатковий функціонал у підменю "Персонажі" (4-й рівень)
def get_hero_details_menu(hero_name):
    """
    Повертає інформацію про конкретного героя.
    :param hero_name: Назва героя
    :return: None (відправляє повідомлення)
    """
    # Тут можна інтегрувати логіку для отримання інформації про героя з бази даних або API
    # Наприклад:
    hero_info = f"**{hero_name}**\n\n📜 Біографія: ...\n⚔️ Навички: ...\n🛠️ Оптимальні білди: ...\n🎮 Ролі в команді: ...\n📊 Статистика: ..."
    return hero_info

# 27. META (4-й рівень)
def get_meta_details_menu(hero_name):
    """
    Повертає детальну інформацію про героя у меті.
    :param hero_name: Назва героя
    :return: None (відправляє повідомлення)
    """
    # Інтеграція з базою даних або API
    meta_info = f"**{hero_name}** в меті:\n\n⚔️ Навички та Сильні Сторони: ...\n📜 Поради щодо Гри: ...\n🛠️ Білди для Мети: ..."
    return meta_info

# 28. Перегляд Турнірів (4-й рівень)
def get_tournament_view_details(tournament_name):
    """
    Повертає детальну інформацію про турнір.
    :param tournament_name: Назва турніру
    :return: None (відправляє повідомлення)
    """
    # Інтеграція з базою даних або API
    tournament_info = f"**{tournament_name}**\n\n🏆 Учасники: ...\n📅 Розклад: ...\n📜 Правила: ...\n📈 Статистика: ..."
    return tournament_info

# Примітка:
# Для повної реалізації всіх 4-х рівнів меню, потрібно обробляти вибір користувача на кожному рівні
# та відповідно відправляти відповідні клавіатури або повідомлення.
# Це зазвичай реалізується через хендлери у основному файлі бота (наприклад, handlers.py).

# Приклад функцій для обробки 4-го рівня меню можна додати у файл handlers.py

# Висновок

Наведений код `keyboards/menus.py` містить повну реалізацію клавіатур для кожного рівня меню вашого телеграм-бота **Mobile-Legends-Starts**. Він охоплює всі рівні меню, кнопки та підменю, згідно з вашою деталізованою деревовидною структурою.

### Додаткові кроки для повної інтеграції:

1. **Створення Хендлерів:**
   - Реалізуйте хендлери для обробки кожної кнопки меню.
   - Використовуйте логіку для відправки відповідних клавіатур або повідомлень при натисканні кнопок.

2. **Використання FSM (Finite State Machine):**
   - Для більш складної навігації між меню можна використовувати FSM для відстеження стану користувача.
   - Це дозволить ефективніше управляти переходами між різними рівнями меню.

3. **Інтеграція з Базою Даних або API:**
   - Для отримання детальної інформації про героїв, турніри та інші дані інтегруйте бот з відповідними джерелами даних.

4. **Оптимізація Клавіатур:**
   - Переконайтеся, що клавіатури не перевантажені кнопками, особливо на 4-му рівні.
   - Для великих списків героїв використовуйте функцію пошуку або пагінацію.

5. **Тестування:**
   - Ретельно протестуйте всі меню та переходи між ними, щоб переконатися в їхній коректній роботі.

### Приклад Хендлерів у `handlers.py`

Нижче наведено приклад того, як можна реалізувати хендлери для обробки меню у вашому основному файлі бота, наприклад, `handlers.py`:

```python
from aiogram import Dispatcher, types
from keyboards.menus import (
    get_main_menu, get_navigation_menu, get_heroes_menu, get_profile_menu,
    get_hero_class_menu, get_builds_menu, get_counter_picks_menu, get_guides_menu,
    get_voting_menu, get_m6_menu, get_gpt_menu, get_meta_menu, get_tournaments_menu,
    get_statistics_menu, get_achievements_menu, get_settings_menu,
    get_feedback_menu, get_help_menu
)
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

# Створіть класи станів для FSM, якщо потрібно

# Приклад обробки команди /start
async def cmd_start(message: types.Message):
    await message.answer("Ласкаво просимо до Mobile-Legends-Starts!", reply_markup=get_main_menu())

# Обробка вибору "Навігація"
async def navigation_handler(message: types.Message):
    if message.text == MenuButton.NAVIGATION.value:
        await message.answer("Виберіть розділ навігації:", reply_markup=get_navigation_menu())

# Обробка вибору "Персонажі"
async def heroes_handler(message: types.Message):
    if message.text == MenuButton.HEROES.value:
        await message.answer("Виберіть клас героя:", reply_markup=get_heroes_menu())

# Обробка вибору класу героя
async def hero_class_handler(message: types.Message):
    if message.text in menu_button_to_class:
        hero_class = menu_button_to_class[message.text]
        await message.answer(f"Вибрано клас: {hero_class}. Виберіть героя:", reply_markup=get_hero_class_menu(hero_class))

# Обробка вибору конкретного героя
async def hero_selection_handler(message: types.Message):
    hero_name = message.text
    if hero_name in sum(heroes_by_class.values(), []):
        hero_details = get_hero_details_menu(hero_name)
        await message.answer(hero_details, reply_markup=get_heroes_menu())

# Обробка вибору "Мій Профіль"
async def profile_handler(message: types.Message):
    if message.text == MenuButton.PROFILE.value:
        await message.answer("Виберіть опцію профілю:", reply_markup=get_profile_menu())

# Обробка інших меню аналогічно...

def register_handlers(dp: Dispatcher):
    dp.register_message_handler(cmd_start, commands="start")
    dp.register_message_handler(navigation_handler, lambda message: message.text == MenuButton.NAVIGATION.value)
    dp.register_message_handler(heroes_handler, lambda message: message.text == MenuButton.HEROES.value)
    dp.register_message_handler(hero_class_handler, lambda message: message.text in menu_button_to_class)
    dp.register_message_handler(hero_selection_handler, lambda message: message.text in sum(heroes_by_class.values(), []))
    dp.register_message_handler(profile_handler, lambda message: message.text == MenuButton.PROFILE.value)
    # Додайте інші хендлери для інших меню
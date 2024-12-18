# keyboards/inline_menus.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_intro_page_1_keyboard() -> InlineKeyboardMarkup:
    """
    Створює інлайн-клавіатуру для першої сторінки вступу з кнопкою 'Далі'.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Далі", callback_data="intro_next_1")
        ]
    ])

def get_intro_page_2_keyboard() -> InlineKeyboardMarkup:
    """
    Створює інлайн-клавіатуру для другої сторінки вступу з кнопкою 'Далі'.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Далі", callback_data="intro_next_2")
        ]
    ])

def get_intro_page_3_keyboard() -> InlineKeyboardMarkup:
    """
    Створює інлайн-клавіатуру для третьої сторінки вступу з кнопкою 'Розпочати'.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Розпочати", callback_data="intro_start")
        ]
    ])

def get_generic_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Створює інлайн-клавіатуру з однією кнопкою '---MLS---'.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="---MLS---", callback_data="mls_button")
        ]
    ])

# Додаємо інлайн-клавіатури для підменю без дублювання кнопок з основного меню

def get_profile_submenu_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Створює інлайн-клавіатуру для підменю профілю з кнопками:
    'Статистика', 'Досягнення', 'Налаштування', 'Зворотній зв'язок', 'Допомога', 'Повернутися'.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📈 Статистика", callback_data="profile_statistics"),
            InlineKeyboardButton(text="🏆 Досягнення", callback_data="profile_achievements")
        ],
        [
            InlineKeyboardButton(text="⚙️ Налаштування", callback_data="profile_settings"),
            InlineKeyboardButton(text="💌 Зворотній зв'язок", callback_data="profile_feedback")
        ],
        [
            InlineKeyboardButton(text="❓ Допомога", callback_data="profile_help")
        ],
        [
            InlineKeyboardButton(text="🔙 Повернутися", callback_data="menu_back")
        ]
    ])

def get_navigation_submenu_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Створює інлайн-клавіатуру для підменю навігації з кнопками:
    'Персонажі', 'Гайди', 'Контр-піки', 'Білди', 'Голосування', 'Повернутися'.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🥷 Персонажі", callback_data="navigate_heroes"),
            InlineKeyboardButton(text="📚 Гайди", callback_data="navigate_guides")
        ],
        [
            InlineKeyboardButton(text="⚖️ Контр-піки", callback_data="navigate_counter_picks"),
            InlineKeyboardButton(text="🛡️ Білди", callback_data="navigate_builds")
        ],
        [
            InlineKeyboardButton(text="📋 Голосування", callback_data="navigate_voting")
        ],
        [
            InlineKeyboardButton(text="🔙 Повернутися", callback_data="menu_back")
        ]
    ])

def get_gpt_submenu_inline_keyboard() -> InlineKeyboardMarkup:
    """
    Створює інлайн-клавіатуру для підменю GPT з кнопками:
    'Генерація Даних', 'Поради', 'Статистика Героїв', 'Повернутися'.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📊 Генерація Даних", callback_data="gpt_data_generation"),
            InlineKeyboardButton(text="💡 Поради", callback_data="gpt_hints")
        ],
        [
            InlineKeyboardButton(text="📈 Статистика Героїв", callback_data="gpt_hero_stats")
        ],
        [
            InlineKeyboardButton(text="🔙 Повернутися", callback_data="menu_back")
        ]
    ])

# Додайте аналогічні функції для інших підменю за потреби, наприклад:
# - get_tournaments_submenu_inline_keyboard()
# - get_meta_submenu_inline_keyboard()
# - get_m6_submenu_inline_keyboard()
# - тощо.
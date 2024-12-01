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

def get_navigation_keyboard() -> InlineKeyboardMarkup:
    """
    Інлайн-клавіатура для навігації з кнопками 'Вперед' і 'Назад'.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Назад", callback_data="nav_back"),
            InlineKeyboardButton(text="Вперед", callback_data="nav_next")
        ]
    ])

def get_confirmation_keyboard() -> InlineKeyboardMarkup:
    """
    Інлайн-клавіатура для підтвердження дії з кнопками 'Так' і 'Ні'.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Так", callback_data="confirm_yes"),
            InlineKeyboardButton(text="Ні", callback_data="confirm_no")
        ]
    ])

def get_profile_actions_keyboard() -> InlineKeyboardMarkup:
    """
    Інлайн-клавіатура для дій у профілі з кнопками 'Змінити ім'я' і 'Переглянути статистику'.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Змінити ім'я", callback_data="profile_change_name"),
            InlineKeyboardButton(text="Переглянути статистику", callback_data="profile_stats")
        ],
        [
            InlineKeyboardButton(text="Назад до меню", callback_data="profile_back")
        ]
    ])

def get_feedback_keyboard() -> InlineKeyboardMarkup:
    """
    Інлайн-клавіатура для вибору типу зворотного зв'язку.
    """
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Залишити відгук", callback_data="feedback_leave"),
            InlineKeyboardButton(text="Повідомити про помилку", callback_data="feedback_bug")
        ],
        [
            InlineKeyboardButton(text="Назад до меню", callback_data="feedback_back")
        ]
    ])

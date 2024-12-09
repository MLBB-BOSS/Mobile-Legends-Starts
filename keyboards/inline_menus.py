# keyboards/inline_menus.py

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

def get_generic_inline_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="MLS Button", callback_data="mls_button")],
            [InlineKeyboardButton(text="Назад до меню", callback_data="menu_back")],
        ]
    )
    return keyboard

def get_intro_page_1_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Далі", callback_data="intro_next_1")],
        ]
    )
    return keyboard

def get_intro_page_2_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Далі", callback_data="intro_next_2")],
        ]
    )
    return keyboard

def get_intro_page_3_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Розпочати", callback_data="intro_start")],
        ]
    )
    return keyboard

# Нижче наведено приклад функції get_main_menu(), яка повертає повноекранну (ReplyKeyboard) клавіатуру.
# Ви можете змінити текст кнопок за потребою.
def get_main_menu():
    # Це прикладова клавіатура головного меню.
    # Залежно від вашої логіки, ви можете додати більше кнопок або змінити їх текст.
    main_menu = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🧭 Навігація"), KeyboardButton(text="🪪 Профіль")],
            [KeyboardButton(text="⚙️ Налаштування"), KeyboardButton(text="❓ Допомога")],
        ],
        resize_keyboard=True
    )
    return main_menu

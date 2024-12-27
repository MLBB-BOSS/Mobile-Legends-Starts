from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

# Ініціалізація бота
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Функції клавіатур
def get_intro_page_1_keyboard():
    """
    Клавіатура для першої сторінки інтро.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Далі", callback_data="intro_next_1")],
        ]
    )
    return keyboard

def get_intro_page_2_keyboard():
    """
    Клавіатура для другої сторінки інтро.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Далі", callback_data="intro_next_2")],
        ]
    )
    return keyboard

def get_intro_page_3_keyboard():
    """
    Клавіатура для третьої сторінки інтро.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Розпочати", callback_data="intro_start")],
        ]
    )
    return keyboard

def get_back_to_main_menu_button():
    """
    Клавіатура з однією кнопкою для повернення до головного меню.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="═══════════════════╗\n║        ░▒▓█ Ｍ Ｌ Ｓ █▓▒░",
                    callback_data="menu_back"
                )
            ]
        ]
    )
    return keyboard

def get_main_menu():
    """
    Генерує клавіатуру для головного меню.
    """
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📰 Новини", callback_data="news_placeholder")],
            [InlineKeyboardButton(text="🎯 Виклики", callback_data="challenges_placeholder")],
        ]
    )
    return keyboard

# Хендлери
@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    """
    Хендлер для команди /start.
    """
    await message.answer(
        text="Вітаємо в MLS боті! Це інтро. Натисніть 'Далі', щоб продовжити.",
        reply_markup=get_intro_page_1_keyboard()
    )

@dp.callback_query_handler(lambda c: c.data == "intro_next_1")
async def intro_page_2(callback_query: types.CallbackQuery):
    """
    Друга сторінка інтро.
    """
    await callback_query.message.edit_text(
        text="Це друга сторінка інтро. Натисніть 'Далі', щоб продовжити.",
        reply_markup=get_intro_page_2_keyboard()
    )

@dp.callback_query_handler(lambda c: c.data == "intro_next_2")
async def intro_page_3(callback_query: types.CallbackQuery):
    """
    Третя сторінка інтро.
    """
    await callback_query.message.edit_text(
        text="Це остання сторінка інтро. Натисніть 'Розпочати', щоб завершити.",
        reply_markup=get_intro_page_3_keyboard()
    )

@dp.callback_query_handler(lambda c: c.data == "intro_start")
async def intro_complete(callback_query: types.CallbackQuery):
    """
    Завершення інтро.
    """
    await callback_query.message.edit_text(
        text="Інтро завершено. Ви можете повернутися до головного меню за допомогою кнопки нижче.",
        reply_markup=get_back_to_main_menu_button()
    )

@dp.callback_query_handler(lambda c: c.data == "menu_back")
async def handle_back_to_main_menu(callback_query: types.CallbackQuery):
    """
    Повернення до головного меню.
    """
    await callback_query.message.edit_text(
        text="Головне меню:",
        reply_markup=get_main_menu()
    )

@dp.callback_query_handler(lambda c: c.data == "news_placeholder")
async def handle_news(callback_query: types.CallbackQuery):
    """
    Обробник для кнопки 'Новини'.
    """
    await callback_query.message.edit_text(
        text="Тут будуть останні новини.",
        reply_markup=get_back_to_main_menu_button()
    )

@dp.callback_query_handler(lambda c: c.data == "challenges_placeholder")
async def handle_challenges(callback_query: types.CallbackQuery):
    """
    Обробник для кнопки 'Виклики'.
    """
    await callback_query.message.edit_text(
        text="Тут будуть ваші виклики.",
        reply_markup=get_back_to_main_menu_button()
    )

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
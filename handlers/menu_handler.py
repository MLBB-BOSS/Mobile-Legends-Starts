from aiogram import Router, Bot
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from states.menu_states import MenuStates

# Текст для меню
NAVIGATION_MENU_TEXT = "🧭 Навігація:\n\nОберіть розділ для переходу."
NAVIGATION_INTERACTIVE_TEXT = "🔍 Інтерактивна інформація про доступні розділи."

# Створення Reply-клавіатури
def get_navigation_menu():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔙 Назад"), KeyboardButton(text="📜 Розділи")],
            [KeyboardButton(text="🗺️ Карта"), KeyboardButton(text="⚙️ Налаштування")],
        ],
        resize_keyboard=True,
    )

# Створення Inline-клавіатури
def get_generic_inline_keyboard():
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📄 Деталі", callback_data="details")],
        [InlineKeyboardButton(text="❌ Закрити", callback_data="close")],
    ])

# Видалення повідомлення з безпечним обробленням винятків
async def safe_delete_message(bot: Bot, chat_id: int, message_id: int):
    try:
        await bot.delete_message(chat_id=chat_id, message_id=message_id)
    except (MessageCantBeDeleted, MessageToDeleteNotFound):
        pass

# Хендлер обробки переходу
router = Router()

@router.message(MenuStates.MAIN_MENU)
async def handle_navigation_transition(message: Message, state: FSMContext, bot: Bot):
    # 1. Видалення повідомлення користувача
    await safe_delete_message(bot, message.chat.id, message.message_id)
    
    # 2. Отримання даних стану
    data = await state.get_data()
    old_message_id = data.get('bot_message_id')
    interactive_message_id = data.get('interactive_message_id')
    
    # 3. Видалення старого "пульта"
    if old_message_id:
        await safe_delete_message(bot, message.chat.id, old_message_id)
    
    # 4. Відправка нового "пульта"
    new_message = await bot.send_message(
        chat_id=message.chat.id,
        text=NAVIGATION_MENU_TEXT,
        reply_markup=get_navigation_menu()
    )
    
    # 5. Оновлення "екрану"
    if interactive_message_id:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=interactive_message_id,
            text=NAVIGATION_INTERACTIVE_TEXT,
            reply_markup=get_generic_inline_keyboard()
        )
    
    # 6. Збереження нового стану
    await state.update_data(
        bot_message_id=new_message.message_id,
        last_text=NAVIGATION_MENU_TEXT,
        last_keyboard=get_navigation_menu()
    )
    await state.set_state(MenuStates.NAVIGATION_MENU)

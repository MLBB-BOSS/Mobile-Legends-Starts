import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext

logger = logging.getLogger(__name__)
router = Router()

# Кнопки ReplyKeyboardMarkup
main_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🧭 Меню"), KeyboardButton(text="🦸 Персонажі")]
    ],
    resize_keyboard=True
)

navigation_menu_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="🔙 Назад")],
        [KeyboardButton(text="🏠 Головне меню")]
    ],
    resize_keyboard=True
)

# InlineKeyboard для "екрану"
navigation_inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Пункт 1", callback_data="nav_1")],
        [InlineKeyboardButton(text="Пункт 2", callback_data="nav_2")]
    ]
)

# Універсальна функція для управління повідомленнями
async def update_interface(bot: Bot, message: Message, state: FSMContext, new_text: str, keyboard: ReplyKeyboardMarkup, inline_text: str, inline_keyboard: InlineKeyboardMarkup):
    # Видаляємо повідомлення користувача
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
    
    # Отримуємо дані стану
    data = await state.get_data()
    old_message_id = data.get('bot_message_id')
    inline_message_id = data.get('inline_message_id')

    # Видаляємо старе повідомлення (пульт керування)
    if old_message_id:
        await bot.delete_message(chat_id=message.chat.id, message_id=old_message_id)
    
    # Відправляємо нове повідомлення з пультом керування
    new_message = await bot.send_message(
        chat_id=message.chat.id,
        text=new_text,
        reply_markup=keyboard
    )
    
    # Редагуємо інлайн повідомлення (екран)
    if inline_message_id:
        await bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=inline_message_id,
            text=inline_text,
            reply_markup=inline_keyboard
        )
    else:
        # Якщо інлайн повідомлення ще немає, відправляємо його
        inline_message = await bot.send_message(
            chat_id=message.chat.id,
            text=inline_text,
            reply_markup=inline_keyboard
        )
        inline_message_id = inline_message.message_id

    # Оновлюємо дані стану
    await state.update_data(
        bot_message_id=new_message.message_id,
        inline_message_id=inline_message_id
    )

# Обробка кнопки "Меню"
@router.message(F.text == "🧭 Меню")
async def handle_main_menu(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"Користувач {message.from_user.id} натиснув кнопку 'Меню'")
    await update_interface(
        bot=bot,
        message=message,
        state=state,
        new_text="Головне меню: оберіть дію.",
        keyboard=main_menu_keyboard,
        inline_text="Інформація головного меню",
        inline_keyboard=InlineKeyboardMarkup()  # Можна додати інлайн клавіатуру для головного меню
    )

# Обробка кнопки "Персонажі"
@router.message(F.text == "🦸 Персонажі")
async def handle_heroes_menu(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"Користувач {message.from_user.id} натиснув кнопку 'Персонажі'")
    await update_interface(
        bot=bot,
        message=message,
        state=state,
        new_text="Тут відображаються персонажі. (Функціонал у розробці)",
        keyboard=main_menu_keyboard,
        inline_text="Інформація про персонажів",
        inline_keyboard=InlineKeyboardMarkup()  # Можна додати інлайн клавіатуру для персонажів
    )

# Обробка кнопки "Навігація"
@router.message(F.text == "🔙 Назад")
async def handle_navigation_menu(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"Користувач {message.from_user.id} натиснув кнопку 'Навігація'")
    await update_interface(
        bot=bot,
        message=message,
        state=state,
        new_text="Навігаційне меню: оберіть пункт.",
        keyboard=navigation_menu_keyboard,
        inline_text="Інформація з навігаційного меню",
        inline_keyboard=navigation_inline_keyboard
    )

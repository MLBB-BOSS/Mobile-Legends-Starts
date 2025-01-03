import logging
from aiogram import Router, F, Bot
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from interface_messages import InterfaceMessages
from navigation_state_manager import NavigationStateManager
from navigation_config import NavigationConfig
from handlers.navigation_errors import handle_navigation_error

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

# Обробка кнопки "Навігація" в головному меню
@router.message(MenuStates.MAIN_MENU, F.text == "🧭 Навігація")
async def handle_navigation_transition(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"Користувач {message.from_user.id} перейшов до навігаційного меню")
    
    # Ініціалізація менеджера станів
    state_manager = NavigationStateManager(state)
    await state_manager.load_state()

    try:
        # Видалення повідомлення користувача
        if not await safe_delete_message(bot, message.chat.id, message.message_id):
            logger.warning(f"Не вдалося видалити повідомлення користувача {message.message_id}")

        # Оновлення інтерфейсу
        new_message_id, new_interactive_id = await update_interface_messages(
            bot=bot,
            chat_id=message.chat.id,
            old_message_id=state_manager.messages.bot_message_id,
            interactive_message_id=state_manager.messages.interactive_message_id,
            state=state
        )

        if new_message_id and new_interactive_id:
            # Оновлення даних повідомлень
            await state_manager.messages.update(
                bot=bot,
                chat_id=message.chat.id,
                new_message_id=new_message_id,
                new_interactive_id=new_interactive_id,
                text=NavigationConfig.Messages.NAVIGATION_MENU,
                keyboard=get_navigation_menu()
            )
            
            # Перехід до нового стану
            await state_manager.transition_to(MenuStates.NAVIGATION_MENU)
            logger.info(f"Успішний перехід до навігаційного меню для користувача {message.from_user.id}")
        else:
            raise ValueError("Не вдалося оновити інтерфейс")

    except Exception as e:
        logger.error(f"Помилка при переході до навігаційного меню: {e}")
        await handle_navigation_error(bot, message.chat.id, state)

# Імпорти з інших файлів
async def handle_navigation_error(bot: Bot, chat_id: int, state: FSMContext):
    try:
        await bot.send_message(
            chat_id=chat_id,
            text=NavigationConfig.Messages.ERROR,
            reply_markup=get_main_menu()
        )
        logger.info(f"Надіслано повідомлення про помилку до чату {chat_id}")
        
        await state.set_state(MenuStates.MAIN_MENU)
        logger.info(f"Стан встановлено на MAIN_MENU для чату {chat_id}")
        
        await state.update_data(
            bot_message_id=None,
            interactive_message_id=None,
            last_text="",
            last_keyboard=None
        )
        logger.info(f"Дані стану очищено для чату {chat_id}")

    except Exception as e:
        logger.critical(f"Критична помилка при обробці помилки навігації: {e}")

# Додайте необхідні класи і змінні з navigation_config.py
class NavigationConfig:
    class Messages:
        NAVIGATION_MENU = "Навігаційне меню: оберіть розділ для переходу"
        INTERACTIVE = "Інтерактивний екран навігації"
        ERROR = "Виникла помилка при обробці команди. Спробуйте ще раз або зверніться до адміністратора."

    class LogMessages:
        TRANSITION_SUCCESS = "Успішний перехід до навігаційного меню для користувача {user_id}"
        TRANSITION_ERROR = "Помилка при переході до навігаційного меню: {error}"
        DELETE_ERROR = "Не вдалося видалити повідомлення {message_id}"
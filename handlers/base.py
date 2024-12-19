import logging
from aiogram import Router, Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.menus import get_main_menu
from texts import START_TEXT, HELP_TEXT, UNKNOWN_COMMAND_TEXT

# Ініціалізація логування
logger = logging.getLogger(__name__)

# Ініціалізація роутера
base_router = Router()

# Стан для базових команд
class BaseStates(StatesGroup):
    MAIN_MENU = State()

# Обробник команди /start
@base_router.message(F.text == "/start")
async def handle_start_command(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"Користувач {message.from_user.id} викликав /start")

    # Відправляємо привітальне повідомлення
    try:
        welcome_message = await bot.send_message(
            chat_id=message.chat.id,
            text=START_TEXT.format(user_first_name=message.from_user.first_name),
            reply_markup=get_main_menu()
        )
        # Зберігаємо ID повідомлення
        await state.update_data(bot_message_id=welcome_message.message_id)
        # Встановлюємо стан до MAIN_MENU
        await state.set_state(BaseStates.MAIN_MENU)
    except Exception as e:
        logger.error(f"Не вдалося надіслати повідомлення /start: {e}")

# Обробник команди /help
@base_router.message(F.text == "/help")
async def handle_help_command(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"Користувач {message.from_user.id} викликав /help")

    # Відправляємо повідомлення з довідкою
    try:
        help_message = await bot.send_message(
            chat_id=message.chat.id,
            text=HELP_TEXT,
            reply_markup=get_main_menu()
        )
        # Зберігаємо ID повідомлення
        await state.update_data(bot_message_id=help_message.message_id)
        # Встановлюємо стан до MAIN_MENU
        await state.set_state(BaseStates.MAIN_MENU)
    except Exception as e:
        logger.error(f"Не вдалося надіслати повідомлення /help: {e}")

# Обробник невідомих команд
@base_router.message(F.text.startswith("/"))
async def handle_unknown_command(message: Message, state: FSMContext, bot: Bot):
    logger.info(f"Користувач {message.from_user.id} викликав невідому команду {message.text}")

    # Відправляємо повідомлення про невідому команду
    try:
        unknown_command_message = await bot.send_message(
            chat_id=message.chat.id,
            text=UNKNOWN_COMMAND_TEXT,
            reply_markup=get_main_menu()
        )
        # Зберігаємо ID повідомлення
        await state.update_data(bot_message_id=unknown_command_message.message_id)
        # Встановлюємо стан до MAIN_MENU
        await state.set_state(BaseStates.MAIN_MENU)
    except Exception as e:
        logger.error(f"Не вдалося надіслати повідомлення про невідому команду: {e}")

# Обробник кнопок у головному меню
@base_router.message(BaseStates.MAIN_MENU)
async def handle_main_menu_buttons(message: Message, state: FSMContext, bot: Bot):
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав {user_choice} в головному меню")

    # Обробка вибору в головному меню
    if user_choice == "🪪 Мій Профіль":
        # Перенаправляємо в модуль обробки профілю
        await state.set_state("profile:PROFILE_MENU")
        await bot.send_message(chat_id=message.chat.id, text="Перехід у меню профілю...")
    elif user_choice == "🌍 Навігація":
        # Перенаправляємо в модуль обробки навігації
        await state.set_state("navigation:NAVIGATION_MENU")
        await bot.send_message(chat_id=message.chat.id, text="Перехід у меню навігації...")
    else:
        await bot.send_message(chat_id=message.chat.id, text=UNKNOWN_COMMAND_TEXT)

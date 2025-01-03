# handlers/tournaments.py
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import F

from keyboards.menus import get_tournaments_menu
from keyboards.inline_menus import get_generic_inline_keyboard
from texts import TOURNAMENTS_MENU_TEXT, TOURNAMENT_VIEW_TEXT, UNKNOWN_COMMAND_TEXT
from states import MenuStates
from utils.message_utils import safe_delete_message, check_and_edit_message, handle_error

router = Router()

@router.message(MenuStates.TOURNAMENTS_MENU)
async def handle_tournaments_menu_buttons(message: Message, state: FSMContext, bot: Bot) -> None:
    """
    Обробчик кнопок у меню Турніри.
    """
    user_choice = message.text
    logger.info(f"Користувач {message.from_user.id} обрав '{user_choice}' в меню Турніри")

    await safe_delete_message(bot, message.chat.id, message.message_id)

    # Логіка обробки вибору користувача
    new_main_text = ""
    new_main_keyboard = get_tournaments_menu()
    new_interactive_text = ""
    new_state = MenuStates.TOURNAMENTS_MENU

    if user_choice == "Створити турнір":
        new_main_text = "🏆 Створення нового турніру..."
        new_interactive_text = "Ви можете створити новий турнір, натиснувши кнопку нижче."
        new_state = MenuStates.CREATE_TOURNAMENT
    elif user_choice == "Переглянути турніри":
        new_main_text = TOURNAMENT_VIEW_TEXT
        new_interactive_text = "Список активних турнірів."
        new_state = MenuStates.VIEW_TOURNAMENTS
    elif user_choice == MenuButton.BACK.value:
        new_main_text = "🧭 Навігаційне меню: оберіть розділ для переходу."
        new_main_keyboard = get_navigation_menu()
        new_interactive_text = "Інтерактивний екран навігації"
        new_state = MenuStates.NAVIGATION_MENU
    else:
        new_main_text = UNKNOWN_COMMAND_TEXT
        new_interactive_text = "Невідома команда"
        new_main_keyboard = get_tournaments_menu()
        new_state = MenuStates.TOURNAMENTS_MENU

    # Відправка нового повідомлення з клавіатурою
    try:
        main_message = await bot.send_message(
            chat_id=message.chat.id,
            text=new_main_text,
            reply_markup=new_main_keyboard
        )
        new_bot_message_id = main_message.message_id
    except Exception as e:
        logger.error(f"Не вдалося надіслати нове повідомлення: {e}")
        await handle_error(bot, chat_id=message.chat.id, error_message=GENERIC_ERROR_MESSAGE_TEXT, logger=logger)
        return

    # Видалення старого повідомлення
    await safe_delete_message(bot, message.chat.id, bot_message_id)

    # Редагування інтерактивного повідомлення
    await check_and_edit_message(
        bot=bot,
        chat_id=message.chat.id,
        message_id=interactive_message_id,
        new_text=new_interactive_text,
        new_keyboard=get_generic_inline_keyboard(),
        state=state
    )

    # Оновлення стану користувача
    await state.update_data(bot_message_id=new_bot_message_id)
    await transition_state(state, new_state)

from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.inline_menus import CallbackData, get_main_inline_keyboard, get_heroes_inline_keyboard, get_guides_inline_keyboard
from utils.menu_messages import MenuMessages
from aiogram.fsm.context import FSMContext
import logging

router = Router()

# Налаштування логування
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def safe_edit_message(callback_message, new_text, reply_markup=None):
    """
    Безпечне редагування повідомлення. Створює нове, якщо редагування неможливе.
    """
    try:
        await callback_message.edit_text(
            text=new_text,
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
    except Exception as e:
        logging.error(f"Failed to edit message {callback_message.message_id}: {e}")
        new_message = await callback_message.chat.send_message(
            text=new_text,
            reply_markup=reply_markup,
            parse_mode="HTML"
        )
        return new_message

@router.callback_query(F.data == CallbackData.HEROES.value)
async def process_heroes_menu(callback: CallbackQuery, state: FSMContext):
    """Обробка натискання кнопки Персонажі"""
    user_id = callback.from_user.id
    logger.info(f"User {user_id} pressed heroes")
    
    menu_text = MenuMessages.get_heroes_menu_text()
    try:
        new_message = await safe_edit_message(
            callback.message,
            f"<b>{menu_text['title']}</b>\n\n{menu_text['description']}",
            reply_markup=get_heroes_inline_keyboard()
        )
        # Збереження останнього повідомлення в FSM
        await state.update_data(last_message_id=new_message.message_id if new_message else callback.message.message_id)
        logger.info(f"Heroes menu updated for user {user_id}")
    except Exception as e:
        logger.error(f"Failed to update heroes menu for user {user_id}: {e}")
        await callback.message.answer("Сталася помилка при оновленні меню. Спробуйте пізніше.")
    
    await callback.answer()

@router.callback_query(F.data == CallbackData.GUIDES.value)
async def process_guides_menu(callback: CallbackQuery, state: FSMContext):
    """Обробка натискання кнопки Гайди"""
    user_id = callback.from_user.id
    logger.info(f"User {user_id} pressed guides")
    
    menu_text = MenuMessages.get_guides_menu_text()
    try:
        new_message = await safe_edit_message(
            callback.message,
            f"<b>{menu_text['title']}</b>\n\n{menu_text['description']}",
            reply_markup=get_guides_inline_keyboard()
        )
        # Збереження останнього повідомлення в FSM
        await state.update_data(last_message_id=new_message.message_id if new_message else callback.message.message_id)
        logger.info(f"Guides menu updated for user {user_id}")
    except Exception as e:
        logger.error(f"Failed to update guides menu for user {user_id}: {e}")
        await callback.message.answer("Сталася помилка при оновленні меню. Спробуйте пізніше.")
    
    await callback.answer()

@router.callback_query(F.data == CallbackData.BACK.value)
async def process_back_button(callback: CallbackQuery, state: FSMContext):
    """Обробка натискання кнопки Назад"""
    user_id = callback.from_user.id
    logger.info(f"User {user_id} pressed back")
    
    main_menu_text = {
        "title": "🎮 Головне меню",
        "description": "Оберіть розділ для навігації:"
    }
    try:
        new_message = await safe_edit_message(
            callback.message,
            f"<b>{main_menu_text['title']}</b>\n\n{main_menu_text['description']}",
            reply_markup=get_main_inline_keyboard()
        )
        # Оновлення стану FSM
        await state.update_data(last_message_id=new_message.message_id if new_message else callback.message.message_id)
        logger.info(f"Returned to main menu for user {user_id}")
    except Exception as e:
        logger.error(f"Failed to return to main menu for user {user_id}: {e}")
        await callback.message.answer("Сталася помилка при поверненні до головного меню. Спробуйте пізніше.")
    
    await callback.answer()

@router.callback_query()
async def handle_unknown_callback(callback: CallbackQuery):
    """Обробка невідомих callback'ів"""
    user_id = callback.from_user.id
    data = callback.data
    logger.warning(f"User {user_id} pressed unknown callback: {data}")
    
    try:
        await callback.answer(
            "Невідома команда. Будь ласка, використовуйте надані кнопки для навігації.",
            show_alert=True
        )
    except Exception as e:
        logger.error(f"Failed to send unknown command response to user {user_id}: {e}")

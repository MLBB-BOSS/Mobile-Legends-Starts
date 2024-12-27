from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
import logging
from texts import TextTemplates
from state_manager import state_manager
from states import MenuStates

# Налаштування логування
logger = logging.getLogger(__name__)
router = Router()

# Константи текстових шаблонів
FEEDBACK_TEXT = TextTemplates.FEEDBACK_TEXT
ERROR_TEXT = """```
┏━━━━━━━━ ПОМИЛКА ━━━━━━━━┓
┃ ❌ Щось пішло не так... ┃
┃ Спробуйте пізніше      ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━┛```"""

@router.message(Command("feedback"))
async def feedback_handler(message: Message, state: FSMContext):
    """
    Обробник команди /feedback
    Показує меню зворотного зв'язку
    """
    try:
        result = await state_manager.transition_state(
            state=state,
            new_state=MenuStates.FEEDBACK,
            additional_data={
                "from_user_id": message.from_user.id,
                "username": message.from_user.username,
                "timestamp": message.date.isoformat()
            }
        )
        
        if result.success:
            await message.answer(
                text=FEEDBACK_TEXT,
                parse_mode="Markdown"
            )
        else:
            logger.error(f"State transition failed: {result.error}")
            await message.answer(
                text=ERROR_TEXT,
                parse_mode="Markdown"
            )
            
    except Exception as e:
        logger.error(f"Feedback handler error: {str(e)}")
        await message.answer(
            text=ERROR_TEXT,
            parse_mode="Markdown"
        )

@router.message(Command("rate"))
async def rate_handler(message: Message, state: FSMContext):
    """
    Обробник команди /rate
    Дозволяє оцінити бота
    """
    try:
        result = await state_manager.transition_state(
            state=state,
            new_state=MenuStates.RATING,
            preserve_data=True
        )
        
        if result.success:
            await message.answer(
                text=TextTemplates.RATING_TEXT,
                parse_mode="Markdown"
            )
        else:
            logger.error(f"Rate handler error: {result.error}")
            await message.answer(
                text=ERROR_TEXT,
                parse_mode="Markdown"
            )
            
    except Exception as e:
        logger.error(f"Rate handler error: {str(e)}")
        await message.answer(
            text=ERROR_TEXT,
            parse_mode="Markdown"
        )

@router.message(Command("suggest"))
async def suggest_handler(message: Message, state: FSMContext):
    """
    Обробник команди /suggest
    Дозволяє надіслати пропозицію
    """
    try:
        result = await state_manager.transition_state(
            state=state,
            new_state=MenuStates.SUGGESTION,
            preserve_data=True
        )
        
        if result.success:
            await message.answer(
                text=TextTemplates.SUGGEST_TEXT,
                parse_mode="Markdown"
            )
        else:
            logger.error(f"Suggest handler error: {result.error}")
            await message.answer(
                text=ERROR_TEXT,
                parse_mode="Markdown"
            )
            
    except Exception as e:
        logger.error(f"Suggest handler error: {str(e)}")
        await message.answer(
            text=ERROR_TEXT,
            parse_mode="Markdown"
        )

@router.message(Command("report"))
async def report_handler(message: Message, state: FSMContext):
    """
    Обробник команди /report
    Дозволяє повідомити про помилку
    """
    try:
        result = await state_manager.transition_state(
            state=state,
            new_state=MenuStates.REPORT,
            preserve_data=True
        )
        
        if result.success:
            await message.answer(
                text=TextTemplates.REPORT_TEXT,
                parse_mode="Markdown"
            )
        else:
            logger.error(f"Report handler error: {result.error}")
            await message.answer(
                text=ERROR_TEXT,
                parse_mode="Markdown"
            )
            
    except Exception as e:
        logger.error(f"Report handler error: {str(e)}")
        await message.answer(
            text=ERROR_TEXT,
            parse_mode="Markdown"
        )

# Обробник для повернення до головного меню
@router.message(Command("menu"))
async def menu_handler(message: Message, state: FSMContext):
    """
    Обробник команди /menu
    Повертає користувача до головного меню
    """
    try:
        result = await state_manager.reset_state(state)
        
        if result.success:
            await message.answer(
                text=TextTemplates.MENU_TEXT,
                parse_mode="Markdown"
            )
        else:
            logger.error(f"Menu handler error: {result.error}")
            await message.answer(
                text=ERROR_TEXT,
                parse_mode="Markdown"
            )
            
    except Exception as e:
        logger.error(f"Menu handler error: {str(e)}")
        await message.answer(
            text=ERROR_TEXT,
            parse_mode="Markdown"
        )

# Обробник невідомих команд
@router.message(F.text.startswith("/"))
async def unknown_command_handler(message: Message):
    """
    Обробник невідомих команд
    """
    await message.answer(
        text=TextTemplates.UNKNOWN_COMMAND_TEXT,
        parse_mode="Markdown"
    )

# Обробник для відстеження помилок
@router.errors()
async def error_handler(update: types.Update, exception: Exception):
    """
    Загальний обробник помилок
    """
    logger.error(f"Update {update} caused error {exception}")

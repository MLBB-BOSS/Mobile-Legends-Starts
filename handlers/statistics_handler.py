# handlers/statistics_handler.py
from aiogram import Router, types, F
from utils.localization import loc
import logging

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == loc.get_message("buttons.statistics"))
async def handle_statistics(message: types.Message):
    try:
        # Placeholder statistics - implement your actual statistics logic here
        user_stats = {
            "games": 0,
            "wins": 0,
            "winrate": 0
        }
        
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=[[
                types.KeyboardButton(text=loc.get_message("buttons.back_to_navigation"))
            ]],
            resize_keyboard=True
        )
        
        await message.answer(
            text=loc.get_message("messages.statistics_info").format(**user_stats),
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Error handling statistics: {e}")
        await message.answer(loc.get_message("errors.general"))

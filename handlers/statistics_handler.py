# handlers/statistics_handler.py
from aiogram import Router, types, F
from utils.localization import loc

router = Router()

@router.message(F.text == loc.get_message("buttons.statistics"))
async def handle_statistics(message: types.Message):
    try:
        # Assuming you have a function to get user statistics
        stats = await get_user_statistics(message.from_user.id)
        
        await message.answer(
            loc.get_message("messages.statistics_info").format(
                games=stats.get('games', 0),
                wins=stats.get('wins', 0),
                winrate=stats.get('winrate', 0)
            )
        )
    except Exception as e:
        await message.answer(loc.get_message("errors.general"))

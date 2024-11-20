# handlers/hero_class_handlers.py
from aiogram import Router, types, F
from utils.localization import loc
import logging

router = Router()
logger = logging.getLogger(__name__)

# Map buttons to hero classes based on localization
HERO_CLASSES = {
    loc.get_message("buttons.tanks"): "tank",
    loc.get_message("buttons.fighters"): "fighter",
    loc.get_message("buttons.assassins"): "assassin",
    loc.get_message("buttons.mages"): "mage",
    loc.get_message("buttons.marksmen"): "marksman",
    loc.get_message("buttons.supports"): "support"
}

@router.message(F.text.in_(HERO_CLASSES.keys()))
async def handle_hero_class_selection(message: types.Message):
    try:
        class_type = HERO_CLASSES[message.text]
        heroes = loc.get_message(f"heroes.classes.{class_type}.heroes")
        
        keyboard = create_hero_keyboard(heroes)
        await message.answer(
            text=loc.get_message("messages.hero_menu.select_hero").format(
                class_name=loc.get_message(f"heroes.classes.{class_type}.name")
            ),
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Error handling hero class selection: {e}")
        await message.answer(loc.get_message("errors.general"))

def create_hero_keyboard(heroes: list) -> types.ReplyKeyboardMarkup:
    keyboard = []
    # Create rows with 2 heroes per row
    for i in range(0, len(heroes), 2):
        row = [types.KeyboardButton(text=heroes[i])]
        if i + 1 < len(heroes):
            row.append(types.KeyboardButton(text=heroes[i + 1]))
        keyboard.append(row)
    
    # Add back button using localized text
    keyboard.append([
        types.KeyboardButton(text=loc.get_message("buttons.back_to_hero_classes"))
    ])
    
    return types.ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )

# Handle hero selection
@router.message(lambda message: any(message.text in class_info["heroes"] 
                                  for class_info in loc.get_message("heroes.classes").values()))
async def handle_hero_selection(message: types.Message):
    try:
        hero_name = message.text
        hero_info = loc.get_message(f"heroes.info.{hero_name}")
        
        keyboard = types.ReplyKeyboardMarkup(
            keyboard=[[
                types.KeyboardButton(text=loc.get_message("buttons.back_to_hero_list"))
            ]],
            resize_keyboard=True
        )
        
        await message.answer(
            text=hero_info,
            reply_markup=keyboard
        )
    except Exception as e:
        logger.error(f"Error handling hero selection: {e}")
        await message.answer(loc.get_message("errors.hero_not_found"))

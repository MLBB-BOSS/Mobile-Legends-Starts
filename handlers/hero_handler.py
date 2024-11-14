# handlers/hero_handler.py
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from services.keyboard_service import get_class_keyboard, get_heroes_keyboard

hero_router = Router()

@hero_router.message(F.text == "/heroes")
async def heroes_command(message: Message):
    """Виводить клавіатуру для вибору класу героїв."""
    await message.reply("Оберіть клас персонажів:", reply_markup=get_class_keyboard())

@hero_router.callback_query(lambda c: c.data and c.data.startswith("class_"))
async def process_class_selection(call: CallbackQuery):
    """Обробляє вибір класу та виводить персонажів цього класу."""
    hero_class = call.data.split("_")[1]
    await call.message.edit_text(f"Оберіть персонажа з класу {hero_class}:", reply_markup=get_heroes_keyboard(hero_class))

@hero_router.callback_query(lambda c: c.data and c.data == "back_to_classes")
async def back_to_classes(call: CallbackQuery):
    """Повертає користувача до вибору класу."""
    await call.message.edit_text("Оберіть клас персонажів:", reply_markup=get_class_keyboard())

@hero_router.callback_query(lambda c: c.data and c.data.startswith("hero_"))
async def process_hero_selection(call: CallbackQuery):
    """Обробляє вибір конкретного персонажа та показує деталі."""
    hero_name = call.data.split("_")[1]
    await call.message.edit_text(f"Ви обрали героя {hero_name}. Додаткова інформація буде додана.")

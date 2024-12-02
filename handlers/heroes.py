# handlers/heroes.py

from aiogram import Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.filters import F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram import Bot

from data.heroes_loader import get_hero_info, get_hero_info_keyboard

router = Router()

@router.message(F.text.startswith("/hero "))
async def show_hero_info(message: Message, state: FSMContext, bot: Bot):
    hero_name = message.text.split("/hero ")[1].strip()
    hero = get_hero_info(hero_name)
    if hero:
        # Форматування тексту інформації про героя
        response_text = f"<b>{hero['name']}</b>\n" \
                        f"Клас: {hero['class']}\n" \
                        f"Тип атаки: {hero['attack_type']}\n" \
                        f"Додаткові ефекти: {hero['additional_effects']}\n\n" \
                        f"<b>Рекомендовані предмети:</b>\n" + "\n".join(hero['recommended_items']) + "\n\n" \
                        f"<b>Базові стати:</b>\n" \
                        f"Здоров'я: {hero['base_stats']['health']}\n" \
                        f"Фізичний урон: {hero['base_stats']['physical_attack']}\n" \
                        f"Фізична броня: {hero['base_stats']['physical_defense']}\n" \
                        f"Магічна броня: {hero['base_stats']['magic_defense']}\n" \
                        f"Швидкість руху: {hero['base_stats']['movement_speed']}\n" \
                        f"Швидкість атаки: {hero['base_stats']['attack_speed']}\n" \
                        f"Регенація здоров'я: {hero['base_stats']['health_regen']}\n" \
                        f"Регенація мани: {hero['base_stats']['mana_regen']}\n\n" \
                        f"<b>Навички:</b>\n"

        for skill_key, skill in hero['skills'].items():
            response_text += f"\n<b>{skill['name']}</b>: {skill['description']}"
            if 'cooldown' in skill:
                response_text += f" (Кулдаун: {skill['cooldown']})"
            if 'mana_cost' in skill:
                response_text += f", Вартість мани: {skill['mana_cost']}"
        
        await bot.send_message(
            chat_id=message.chat.id,
            text=response_text,
            parse_mode="HTML",
            reply_markup=get_hero_info_keyboard(hero['name'])
        )
    else:
        await bot.send_message(
            chat_id=message.chat.id,
            text="Герой з таким ім'ям не знайдений. Будь ласка, перевірте правильність введення.",
            reply_markup=get_generic_inline_keyboard()
        )

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from services.keyboard_service import get_class_keyboard
import logging

logger = logging.getLogger(__name__)
router = Router(name="message_router")

@router.message(F.text == "🦸‍♂️ Герої")
async def handle_heroes_button(message: Message):
    try:
        await message.answer(
            "Оберіть клас героя:",
            reply_markup=get_class_keyboard()
        )
        logger.info(f"Показано меню героїв для користувача {message.from_user.id}")
    except Exception as e:
        logger.error(f"Помилка при показі меню героїв: {e}")
        await message.answer("Вибачте, сталася помилка. Спробуйте пізніше.")

@router.message(F.text == "🎯 Мета")
async def handle_meta_button(message: Message):
    try:
        await message.answer(
            "*Актуальний мета-звіт:*\n\n"
            "🥇 *Топ Тір:*\n"
            "• Tank: Tigreal, Franco\n"
            "• Fighter: Alucard, Zilong\n"
            "• Assassin: Saber, Karina\n"
            "• Mage: Eudora, Aurora\n"
            "• Marksman: Layla, Bruno\n"
            "• Support: Rafaela, Angela",
            parse_mode="Markdown"
        )
        logger.info(f"Показано мета-звіт для користувача {message.from_user.id}")
    except Exception as e:
        logger.error(f"Помилка при показі мета-звіту: {e}")
        await message.answer("Вибачте, сталася помилка. Спробуйте пізніше.")

@router.message(F.text == "🛠️ Білди")
async def handle_builds_button(message: Message):
    try:
        await message.answer(
            "Оберіть героя для перегляду білдів:\n"
            "(Функція в розробці)",
        )
        logger.info(f"Показано меню білдів для користувача {message.from_user.id}")
    except Exception as e:
        logger.error(f"Помилка при показі меню білдів: {e}")
        await message.answer("Вибачте, сталася помилка. Спробуйте пізніше.")

@router.message(F.text == "❓ Допомога")
async def handle_help_button(message: Message):
    try:
        help_text = '''
*Як користуватися ботом:*

• Використовуйте кнопки внизу екрану для навігації
• У розділі "Герої" ви знайдете інформацію про всіх героїв
• "Мета" покаже актуальний tier list
• "Білди" містить рекомендовані збірки для героїв

*Додаткові команди:*
/start - перезапустити бота
/help - показати це повідомлення

*Потрібна додаткова допомога?*
Напишіть "допомога" в чат
'''
        await message.answer(help_text, parse_mode="Markdown")
        logger.info(f"Показано довідку для користувача {message.from_user.id}")
    except Exception as e:
        logger.error(f"Помилка при показі довідки: {e}")
        await message.answer("Вибачте, сталася помилка. Спробуйте пізніше.")

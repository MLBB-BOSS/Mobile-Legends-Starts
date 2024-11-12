# handlers/user/profile_handler.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ..base_handler import BaseHandler
from database.repositories import UserRepository
from models import User

class ProfileHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.user_repository = UserRepository()

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обробка команди перегляду профілю"""
        try:
            with db.get_session() as session:
                # Якщо є аргумент - шукаємо профіль по username
                if context.args and len(context.args) > 0:
                    username = context.args[0].strip('@')
                    user = self.user_repository.get_by_username(session, username)
                else:
                    # Інакше показуємо профіль поточного користувача
                    user = self.user_repository.get_by_telegram_id(
                        session, 
                        update.effective_user.id
                    )

                if not user:
                    await update.message.reply_text("❌ Профіль не знайдено")
                    return

                # Формуємо текст профілю
                profile_text = (
                    f"👤 *Профіль користувача*\n"
                    f"Нік: @{user.username}\n"
                    f"Рівень: {user.level} ({user.experience} XP)\n"
                    f"Досягнення: {len(user.achievements)}\n"
                )

                if user.bio:
                    profile_text += f"\n📝 Про себе:\n{user.bio}\n"

                # Створюємо клавіатуру
                keyboard = [
                    [
                        InlineKeyboardButton("🏆 Досягнення", callback_data=f"achievements_{user.id}"),
                        InlineKeyboardButton("📊 Статистика", callback_data=f"stats_{user.id}")
                    ]
                ]

                # Додаємо кнопку редагування тільки для власного профілю
                if update.effective_user.id == user.telegram_id:
                    keyboard.append([
                        InlineKeyboardButton("✏️ Редагувати профіль", callback_data="edit_profile")
                    ])

                reply_markup = InlineKeyboardMarkup(keyboard)

                await update.message.reply_text(
                    profile_text,
                    parse_mode='Markdown',
                    reply_markup=reply_markup
                )

        except Exception as e:
            await self.handle_error(update, context, e)

    async def handle_edit_profile(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обробка редагування профілю"""
        query = update.callback_query
        await query.answer()

        keyboard = [
            [
                InlineKeyboardButton("📝 Змінити опис", callback_data="edit_bio"),
                InlineKeyboardButton("🔙 Назад", callback_data="back_to_profile")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.edit_text(
            "✏️ Що ви хочете змінити у своєму профілі?",
            reply_markup=reply_markup
        )

    async def handle_edit_bio(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обробка зміни опису профілю"""
        query = update.callback_query
        await query.answer()

        context.user_data['editing_bio'] = True
        await query.message.edit_text(
            "📝 Надішліть новий опис вашого профілю.\n"
            "Для скасування напишіть /cancel"
        )

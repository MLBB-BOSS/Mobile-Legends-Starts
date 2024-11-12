# handlers/moderation/vote_handler.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ..base_handler import BaseHandler
from database.repositories import UserRepository
from datetime import datetime, timedelta

class VoteHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.user_repository = UserRepository()
        self.active_votes = {}  # Зберігаємо активні голосування

    async def handle_create_vote(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Створення нового голосування"""
        try:
            if not await self.check_admin_rights(update.effective_user.id):
                await update.message.reply_text("❌ У вас немає прав для створення голосування")
                return

            if len(context.args) < 2:
                await update.message.reply_text(
                    "❌ Використання: /createvote <тема> <варіант1> <варіант2> ..."
                )
                return

            topic = context.args[0]
            options = context.args[1:]

            # Створюємо нове голосування
            vote_id = str(datetime.now().timestamp())
            self.active_votes[vote_id] = {
                'topic': topic,
                'options': {option: [] for option in options},
                'created_by': update.effective_user.id,
                'expires_at': datetime.now() + timedelta(hours=24)
            }

            # Створюємо клавіатуру з варіантами
            keyboard = []
            for option in options:
                keyboard.append([
                    InlineKeyboardButton(
                        f"{option} (0)", 
                        callback_data=f"vote_{vote_id}_{option}"
                    )
                ])

            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(
                f"📊 *Нове голосування:* {topic}\n"
                f"Голосування закінчиться через 24 години\n\n"
                "Оберіть ваш варіант:",
                parse_mode='Markdown',
                reply_markup=reply_markup
            )

        except Exception as e:
            await self.handle_error(update, context, e)

    async def handle_vote(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обробка голосу"""
        query = update.callback_query
        await query.answer()

        try:
            _, vote_id, option = query.data.split('_')
            vote = self.active_votes.get(vote_id)

            if not vote:
                await query.message.edit_text("❌ Голосування не знайдено або закінчилось")
                return

            if datetime.now() > vote['expires_at']:
                await query.message.edit_text("❌ Голосування закінчилось")
                return

            user_id = update.effective_user.id

            # Видаляємо попередній голос користувача
            for opt in vote['options']:
                if user_id in vote['options'][opt]:
                    vote['options'][opt].remove(user_id)

            # Додаємо новий голос
            vote['options'][option].append(user_id)

            # Оновлюємо клавіатуру
            keyboard = []
            for opt in vote['options']:
                votes_count = len(vote['options'][opt])
                keyboard.append([
                    InlineKeyboardButton(
                        f"{opt} ({votes_count})", 
                        callback_data=f"vote_{vote_id}_{opt}"
                    )
                ])

            reply_markup = InlineKeyboardMarkup(keyboard)

            # Оновлюємо повідомлення
            await query.message.edit_reply_markup(reply_markup=reply_markup)

        except Exception as e:
            await self.handle_error(update, context, e)

    async def check_admin_rights(self, user_id: int) -> bool:
        """Перевірка прав адміністратора"""
        with db.get_session() as session:
            user = self.user_repository.get_by_telegram_id(session, user_id)
            return user and user.is_admin

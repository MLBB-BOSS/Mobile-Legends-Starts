# handlers/moderation/moderation_handler.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ..base_handler import BaseHandler
from database.repositories import UserRepository
from datetime import datetime, timedelta

class ModerationHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.user_repository = UserRepository()
        self.warnings = {}  # Зберігаємо попередження користувачів

    async def handle_warn(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Видача попередження користувачу"""
        try:
            if not await self.check_moderator_rights(update.effective_user.id):
                await update.message.reply_text("❌ У вас немає прав модератора")
                return

            if len(context.args) < 2:
                await update.message.reply_text(
                    "❌ Використання: /warn @username <причина>"
                )
                return

            target_username = context.args[0].strip('@')
            reason = ' '.join(context.args[1:])

            with db.get_session() as session:
                target_user = self.user_repository.get_by_username(session, target_username)
                
                if not target_user:
                    await update.message.reply_text("❌ Користувача не знайдено")
                    return

                # Додаємо попередження
                if target_user.telegram_id not in self.warnings:
                    self.warnings[target_user.telegram_id] = []

                self.warnings[target_user.telegram_id].append({
                    'reason': reason,
                    'timestamp': datetime.now(),
                    'by': update.effective_user.id
                })

                warning_count = len(self.warnings[target_user.telegram_id])

                # Перевіряємо кількість попереджень
                if warning_count >= 3:
                    # Блокуємо користувача
                    await self.handle_ban(update, context, target_user.telegram_id)
                    return

                await update.message.reply_text(
                    f"⚠️ Користувач @{target_username} отримав попередження.\n"
                    f"Причина: {reason}\n"
                    f"Кількість попереджень: {warning_count}/3"
                )

        except Exception as e:
            await self.handle_error(update, context, e)

    async def handle_ban(self, update: Update, context: ContextTypes.DEFAULT_TYPE, 
                        user_id: int = None) -> None:
        """Блокування користувача"""
        try:
            if not await self.check_moderator_rights(update.effective_user.id):
                await update.message.reply_text("❌ У вас немає прав модератора")
                return

            target_id = user_id
            reason = "Перевищення кількості попереджень"

            if not target_id:
                if len(context.args) < 2:
                    await update.message.reply_text(
                        "❌ Використання: /ban @username <причина>"
                    )
                    return
                
                target_username = context.args[0].strip('@')
                reason = ' '.join(context.args[1:])

                with db.get_session() as session:
                    target_user = self.user_repository.get_by_username(
                        session, 
                        target_username
                    )
                    if target_user:
                        target_id = target_user.telegram_id

            if not target_id:
                await update.message.reply_text("❌ Користувача не знайдено")
                return

            with db.get_session() as session:
                # Оновлюємо статус користувача
                self.user_repository.update(
                    session,
                    target_id,
                    is_banned=True,
                    ban_reason=reason,
                    banned_at=datetime.now()
                )

            await update.message.reply_text(
                f"🚫 Користувача заблоковано\n"
                f"Причина: {reason}"
            )

        except Exception as e:
            await self.handle_error(update, context, e)

    async def handle_unban(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Розблокування користувача"""
        try:
            if not await self.check_moderator_rights(update.effective_user.id):
                await update.message.reply_text("❌ У вас немає прав модератора")
                return

            if not context.args:
                await update.message.reply_text("❌ Використання: /unban @username")
                return

            target_username = context.args[0].strip('@')

            with db.get_session() as session:
                target_user = self.user_repository.get_by_username(session, target_username)
                
                if not target_user:
                    await update.message.reply_text("❌ Користувача не знайдено")
                    return

                # Оновлюємо статус користувача
                self.user_repository.update(
                    session,
                    target_user.id,
                    is_banned=False,
                    ban_reason=None,
                    banned_at=None
                )

            await update.message.reply_text(
                f"✅ Користувача @{target_username} розблоковано"
            )

        except Exception as e:
            await self.handle_error(update, context, e)

    async def check_moderator_rights(self, user_id: int) -> bool:
        """Перевірка прав модератора"""
        with db.get_session() as session:
            user = self.user_repository.get_by_telegram_id(session, user_id)
            return user and (user.is_admin or user.is_moderator)

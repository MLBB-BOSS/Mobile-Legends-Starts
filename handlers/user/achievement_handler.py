# handlers/user/achievement_handler.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ..base_handler import BaseHandler
from database.repositories import UserRepository, AchievementRepository

class AchievementHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.user_repository = UserRepository()
        self.achievement_repository = AchievementRepository()

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обробка команди перегляду досягнень"""
        try:
            with db.get_session() as session:
                user = self.user_repository.get_by_telegram_id(
                    session, 
                    update.effective_user.id
                )
                
                if not user:
                    await update.message.reply_text("❌ Користувача не знайдено")
                    return

                achievements = self.achievement_repository.get_user_achievements(
                    session, 
                    user.id
                )

                if not achievements:
                    await update.message.reply_text(
                        "🏆 У вас поки що немає досягнень.\n"
                        "Беріть участь в активностях, щоб отримувати нові досягнення!"
                    )
                    return

                # Групуємо досягнення за категоріями
                achievement_text = "🏆 *Ваші досягнення:*\n\n"
                total_points = 0

                # Сортуємо досягнення за кількістю очків
                sorted_achievements = sorted(
                    achievements, 
                    key=lambda x: x.points, 
                    reverse=True
                )

                for achievement in sorted_achievements:
                    achievement_text += (
                        f"• {achievement.name} (+{achievement.points} очків)\n"
                        f"  _{achievement.description}_\n\n"
                    )
                    total_points += achievement.points

                achievement_text += f"\n📊 Загальна кількість очків: {total_points}"

                # Створюємо клавіатуру
                keyboard = [
                    [
                        InlineKeyboardButton(
                            "🎯 Доступні досягнення", 
                            callback_data="available_achievements"
                        )
                    ],
                    [
                        InlineKeyboardButton(
                            "🏅 Рейтинг гравців", 
                            callback_data="achievements_leaderboard"
                        )
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                await update.message.reply_text(
                    achievement_text,
                    parse_mode='Markdown',
                    reply_markup=reply_markup
                )

        except Exception as e:
            await self.handle_error(update, context, e)

    async def handle_available_achievements(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Показ доступних досягнень"""
        query = update.callback_query
        await query.answer()

        try:
            with db.get_session() as session:
                user = self.user_repository.get_by_telegram_id(
                    session, 
                    update.effective_user.id
                )
                
                all_achievements = self.achievement_repository.get_all(session)
                user_achievements = set(user.achievements)
                
                # Фільтруємо досягнення, які ще не отримані
                available = [a for a in all_achievements if a not in user_achievements]
                
                if not available:
                    await query.message.edit_text(
                        "🎉 Вітаємо! Ви отримали всі доступні досягнення!"
                    )
                    return

                text = "🎯 *Доступні досягнення:*\n\n"
                for achievement in available:
                    text += (
                        f"• {achievement.name} (+{achievement.points} очків)\n"
                        f"  _{achievement.description}_\n\n"
                    )

                keyboard = [[
                    InlineKeyboardButton("🔙 Назад", callback_data="back_to_achievements")
                ]]
                reply_markup = InlineKeyboardMarkup(keyboard)

                await query.message.edit_text(
                    text,
                    parse_mode='Markdown',
                    reply_markup=reply_markup
                )

        except Exception as e:
            await self.handle_error(update, context, e)

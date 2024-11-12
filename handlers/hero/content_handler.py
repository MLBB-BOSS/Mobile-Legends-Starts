# handlers/hero/content_handler.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ..base_handler import BaseHandler
from database.repositories import HeroRepository
from services.s3_service import S3Service
from models import Hero, HeroMedia, MediaType

class HeroContentHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.hero_repository = HeroRepository()
        self.s3_service = S3Service()

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обробка команди для отримання контенту героя"""
        try:
            # Отримуємо ім'я героя з аргументів команди
            if not context.args or len(context.args) < 1:
                raise ValueError("Будь ласка, вкажіть ім'я героя")
            
            hero_name = " ".join(context.args)
            
            with db.get_session() as session:
                hero = self.hero_repository.get_with_media(session, hero_name)
                
                if not hero:
                    await update.message.reply_text("❌ Героя не знайдено")
                    return

                # Створюємо клавіатуру для вибору типу контенту
                keyboard = [
                    [
                        InlineKeyboardButton("📸 Скріншоти", callback_data=f"hero_media_{hero.id}_screenshot"),
                        InlineKeyboardButton("🎥 Відео", callback_data=f"hero_media_{hero.id}_video")
                    ],
                    [InlineKeyboardButton("📖 Гайди", callback_data=f"hero_guides_{hero.id}")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)

                # Відправляємо інформацію про героя
                message = (
                    f"🦸‍♂️ *{hero.name}*\n"
                    f"Роль: {hero.role.value}\n"
                    f"Складність: {'⭐' * hero.difficulty}\n\n"
                    f"{hero.description}\n\n"
                    "Оберіть тип контенту:"
                )
                
                await update.message.reply_text(
                    message,
                    parse_mode='Markdown',
                    reply_markup=reply_markup
                )

        except Exception as e:
            await self.handle_error(update, context, e)

    async def handle_media_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обробка callback запиту для медіа контенту"""
        query = update.callback_query
        await query.answer()
        
        try:
            _, hero_id, media_type = query.data.split('_')
            
            with db.get_session() as session:
                hero = self.hero_repository.get_with_media(session, int(hero_id))
                if not hero:
                    await query.message.edit_text("❌ Героя не знайдено")
                    return

                media_items = [m for m in hero.media if m.media_type == MediaType(media_type)]
                
                if not media_items:
                    await query.message.edit_text(
                        f"Для героя {hero.name} поки що немає {media_type} контенту"
                    )
                    return

                # Відправляємо медіа контент
                for media in media_items[:5]:  # Обмежуємо кількість медіа
                    if media.media_type == MediaType.VIDEO:
                        await query.message.reply_video(media.url)
                    else:
                        await query.message.reply_photo(media.url)

        except Exception as e:
            await self.handle_error(update, context, e)

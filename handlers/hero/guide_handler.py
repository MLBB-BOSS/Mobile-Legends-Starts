# handlers/hero/guide_handler.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ..base_handler import BaseHandler
from database.repositories import HeroRepository
from models import HeroGuide

class HeroGuideHandler(BaseHandler):
    def __init__(self):
        super().__init__()
        self.hero_repository = HeroRepository()

    async def handle(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обробка команди для роботи з гайдами героїв"""
        try:
            if not context.args or len(context.args) < 1:
                raise ValueError("Будь ласка, вкажіть ім'я героя")
            
            hero_name = " ".join(context.args)
            
            with db.get_session() as session:
                hero = self.hero_repository.get_with_guides(session, hero_name)
                
                if not hero:
                    await update.message.reply_text("❌ Героя не знайдено")
                    return

                if not hero.guides:
                    keyboard = [[
                        InlineKeyboardButton(
                            "📝 Створити гайд", 
                            callback_data=f"create_guide_{hero.id}"
                        )
                    ]]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    
                    await update.message.reply_text(
                        f"Для героя {hero.name} поки що немає гайдів.\n"
                        "Хочете створити перший?",
                        reply_markup=reply_markup
                    )
                    return

                # Показуємо список гайдів
                guides_text = f"📚 Гайди для героя {hero.name}:\n\n"
                for guide in hero.guides:
                    guides_text += (
                        f"📖 {guide.title}\n"
                        f"👤 Автор: {guide.author.username}\n"
                        f"⭐ Рейтинг: {guide.rating}\n\n"
                    )

                keyboard = [
                    [InlineKeyboardButton("📝 Створити гайд", callback_data=f"create_guide_{hero.id}")],
                    [InlineKeyboardButton("🔍 Детальніше", callback_data=f"view_guides_{hero.id}")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(
                    guides_text,
                    reply_markup=reply_markup
                )

        except Exception as e:
            await self.handle_error(update, context, e)

    async def handle_create_guide(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        """Обробка створення нового гайду"""
        query = update.callback_query
        await query.answer()
        
        try:
            _, hero_id = query.data.split('_')
            
            # Зберігаємо стан користувача для створення гайду
            context.user_data['creating_guide_for'] = int(hero_id)
            
            await query.message.edit_text(
                "📝 Давайте створимо гайд!\n"
                "Надішліть назву гайду одним повідомленням."
            )
            
            # Встановлюємо наступний крок - очікування назви гайду
            return 'WAITING_GUIDE_TITLE'

        except Exception as e:
            await self.handle_error(update, context, e)

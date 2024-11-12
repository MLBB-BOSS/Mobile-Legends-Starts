from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler
from telegram.constants import ParseMode
import logging
from typing import List, Optional, Tuple
from datetime import datetime

from services.hero_service import HeroService
from services.s3_service import S3Service
from models.hero_media import HeroMedia

logger = logging.getLogger(__name__)

class HeroContentHandler:
    def __init__(self, hero_service: HeroService, s3_service: S3Service):
        self.hero_service = hero_service
        self.s3_service = s3_service
        self.ITEMS_PER_PAGE = 5

    async def handle_media_upload(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обробка завантаження медіа файлів"""
        try:
            # Перевірка наявності фото
            if not update.message.photo:
                await update.message.reply_text("Будь ласка, надішліть фотографію героя.")
                return

            # Отримання найбільшого розміру фото
            photo = update.message.photo[-1]
            
            # Отримання файлу
            file = await context.bot.get_file(photo.file_id)
            file_data = await file.download_as_bytearray()

            # Отримання hero_id з контексту користувача
            hero_id = context.user_data.get('current_hero_id')
            if not hero_id:
                await update.message.reply_text("Спочатку виберіть героя використовуючи /select_hero")
                return

            # Завантаження медіа
            hero_media = await self.hero_service.add_hero_media(
                hero_id=hero_id,
                file_data=file_data,
                media_type='screenshot',
                author_id=str(update.effective_user.id),
                author_nickname=update.effective_user.username or update.effective_user.first_name,
                metadata={
                    'telegram_file_id': photo.file_id,
                    'width': photo.width,
                    'height': photo.height
                }
            )

            if hero_media:
                keyboard = self._create_media_keyboard(hero_media)
                await update.message.reply_text(
                    "✅ Фото успішно завантажено! Очікує підтвердження модератора.",
                    reply_markup=keyboard
                )
            else:
                await update.message.reply_text("❌ Помилка при завантаженні фото. Спробуйте ще раз.")

        except Exception as e:
            logger.error(f"Error handling media upload: {e}")
            await update.message.reply_text("Сталася помилка при завантаженні. Спробуйте пізніше.")

    async def handle_media_navigation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обробка навігації по медіа"""
        try:
            query = update.callback_query
            action = query.data.split('_')[1]

            if action == "nav":
                new_index = int(query.data.split('_')[2])
                hero_id = context.user_data.get('current_hero_id')
                
                if not hero_id:
                    await query.answer("Спочатку виберіть героя")
                    return

                media_list = await self.hero_service.get_hero_media(hero_id)
                
                if not media_list:
                    await query.answer("Медіа контент відсутній")
                    return

                start_idx = new_index * self.ITEMS_PER_PAGE
                end_idx = start_idx + self.ITEMS_PER_PAGE
                current_page = media_list[start_idx:end_idx]
                
                keyboard = self._create_media_navigation_keyboard(
                    new_index,
                    len(media_list),
                    self.ITEMS_PER_PAGE
                )

                media_text = self._format_media_list(current_page)
                
                await query.message.edit_text(
                    media_text,
                    reply_markup=keyboard,
                    parse_mode=ParseMode.HTML
                )
                await query.answer()

            elif action == "vote":
                media_id = query.data.split('_')[2]
                success = await self.hero_service.vote_for_media(
                    media_id,
                    str(update.effective_user.id)
                )
                
                if success:
                    await query.answer("Ваш голос враховано!")
                else:
                    await query.answer("Ви вже голосували за це медіа")

            elif action == "delete":
                media_id = query.data.split('_')[2]
                if await self._can_delete_media(update.effective_user.id, media_id):
                    await self._delete_media(media_id)
                    await query.message.edit_text("Медіа контент видалено")
                else:
                    await query.answer("У вас немає прав для видалення цього контенту")

        except Exception as e:
            logger.error(f"Error in media navigation: {e}")
            await query.answer("Сталася помилка. Спробуйте пізніше.")

    def _create_media_keyboard(self, media: HeroMedia) -> InlineKeyboardMarkup:
        """Створення клавіатури для медіа"""
        keyboard = [
            [
                InlineKeyboardButton("👍 Голосувати", callback_data=f"media_vote_{media.id}"),
                InlineKeyboardButton("🗑 Видалити", callback_data=f"media_delete_{media.id}")
            ],
            [
                InlineKeyboardButton("📊 Статистика", callback_data=f"media_stats_{media.id}")
            ]
        ]
        return InlineKeyboardMarkup(keyboard)

    def _create_media_navigation_keyboard(self, 
                                       current_page: int,
                                       total_items: int,
                                       items_per_page: int) -> InlineKeyboardMarkup:
        """Створення клавіатури для навігації по медіа"""
        total_pages = (total_items + items_per_page - 1) // items_per_page
        keyboard = []

        # Кнопки навігації
        nav_buttons = []
        if current_page > 0:
            nav_buttons.append(
                InlineKeyboardButton("⬅️", callback_data=f"media_nav_{current_page-1}")
            )
        nav_buttons.append(
            InlineKeyboardButton(f"{current_page + 1}/{total_pages}", callback_data="media_page")
        )
        if current_page < total_pages - 1:
            nav_buttons.append(
                InlineKeyboardButton("➡️", callback_data=f"media_nav_{current_page+1}")
            )
        keyboard.append(nav_buttons)

        return InlineKeyboardMarkup(keyboard)

    def _format_media_list(self, media_list: List[HeroMedia]) -> str:
        """Форматування списку медіа для відображення"""
        if not media_list:
            return "Медіа контент відсутній"

        result = ["<b>Медіа контент:</b>\n"]
        for i, media in enumerate(media_list, 1):
            status = "✅" if media.approved else "⏳"
            result.append(
                f"{i}. {status} Автор: {media.author_nickname}\n"
                f"   👍 {media.votes} голосів\n"
                f"   📅 {media.added_at.strftime('%d.%m.%Y %H:%M')}\n"
            )
        return "\n".join(result)

    async def _can_delete_media(self, user_id: int, media_id: str) -> bool:
        """Перевірка прав на видалення медіа"""
        # TODO: Додати перевірку прав адміністратора
        media = await self.hero_service.get_hero_media_by_id(media_id)
        return media and str(user_id) == media.author_id

    async def _delete_media(self, media_id: str) -> bool:
        """Видалення медіа"""
        media = await self.hero_service.get_hero_media_by_id(media_id)
        if media:
            # Видалення файлу з S3
            file_key = self.s3_service.get_file_key_from_url(media.url)
            if file_key:
                await self.s3_service.delete_file(file_key)
            
            # Видалення з бази даних
            return await self.hero_service.delete_hero_media(media_id)
        return False

    def get_handlers(self):
        """Отримання всіх обробників"""
        return [
            MessageHandler(filters.PHOTO, self.handle_media_upload),
            CallbackQueryHandler(self.handle_media_navigation, pattern='^media_')
        ]

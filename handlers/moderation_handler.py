# handlers/moderation_handler.py

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler
from telegram.error import TelegramError
import logging
from typing import List, Dict, Optional
from datetime import datetime
from services.hero_service import HeroService
from models.hero_media import HeroMedia

logger = logging.getLogger(__name__)

class ModerationHandler:
    def __init__(self, hero_service: HeroService, moderator_ids: List[str]):
        self.hero_service = hero_service
        self.moderator_ids = set(moderator_ids)  # Використовуємо set для швидшого пошуку
        self.pending_media: Dict[str, List[HeroMedia]] = {}
        self.ITEMS_PER_PAGE = 10

    def is_moderator(self, user_id: str) -> bool:
        """Перевірка чи користувач є модератором"""
        return user_id in self.moderator_ids

    async def moderation_panel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Відображення панелі модерації"""
        try:
            user_id = str(update.effective_user.id)
            if not self.is_moderator(user_id):
                await update.message.reply_text(
                    "⛔️ У вас немає прав модератора."
                )
                return

            # Отримуємо статистику модерації
            stats = await self.hero_service.get_moderation_stats()
            pending_media_list = await self.hero_service.get_pending_media(
                limit=self.ITEMS_PER_PAGE
            )

            if not pending_media_list:
                stats_text = (
                    "📊 Статистика модерації:\n"
                    f"✅ Схвалено сьогодні: {stats['approved_today']}\n"
                    f"❌ Відхилено сьогодні: {stats['rejected_today']}\n"
                    f"⏳ Очікують модерації: {stats['pending_total']}\n\n"
                    "На даний момент немає медіа для модерації."
                )
                await update.message.reply_text(stats_text)
                return

            # Зберігаємо медіа в кеш
            self.pending_media[user_id] = pending_media_list
            context.user_data['moderation_index'] = 0
            context.user_data['moderation_start_time'] = datetime.utcnow()

            await self._show_current_media(update, context, user_id)

        except Exception as e:
            logger.error(f"Error in moderation panel: {e}")
            await update.message.reply_text(
                "❌ Виникла помилка при завантаженні панелі модерації."
            )

    async def handle_moderation_action(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обробка дій модератора"""
        try:
            query = update.callback_query
            user_id = str(update.effective_user.id)

            if not self.is_moderator(user_id):
                await query.answer("⛔️ У вас немає прав модератора.")
                return

            action = query.data.split('_')[1]
            index = context.user_data.get('moderation_index', 0)
            media_list = self.pending_media.get(user_id, [])

            if not media_list:
                await query.answer("Список медіа порожній.")
                return

            media = media_list[index]

            if action in ["approve", "reject"]:
                reason = None
                if action == "reject":
                    # Запитуємо причину відхилення
                    context.user_data['awaiting_rejection_reason'] = media.id
                    keyboard = [
                        [InlineKeyboardButton(reason, callback_data=f"reason_{i}")]
                        for i, reason in enumerate([
                            "Неякісне фото", "Невідповідний контент",
                            "Порушення правил", "Спам"
                        ])
                    ]
                    await query.edit_message_reply_markup(
                        reply_markup=InlineKeyboardMarkup(keyboard)
                    )
                    return

                result = await self._process_moderation(
                    media_id=media.id,
                    action=action,
                    moderator_id=user_id,
                    reason=reason
                )
                
                if result:
                    # Видаляємо оброблене медіа з кешу
                    media_list.pop(index)
                    if not media_list:
                        # Завантажуємо нову порцію медіа
                        new_media = await self.hero_service.get_pending_media(
                            limit=self.ITEMS_PER_PAGE
                        )
                        if new_media:
                            self.pending_media[user_id] = new_media
                            context.user_data['moderation_index'] = 0
                        else:
                            await query.edit_message_text("Модерація завершена!")
                            return

            elif action == "next":
                if index < len(media_list) - 1:
                    context.user_data['moderation_index'] += 1
                else:
                    # Завантажуємо наступну порцію медіа
                    new_media = await self.hero_service.get_pending_media(
                        limit=self.ITEMS_PER_PAGE,
                        offset=len(media_list)
                    )
                    if new_media:
                        self.pending_media[user_id].extend(new_media)
                        context.user_data['moderation_index'] += 1
                    else:
                        await query.answer("Це останнє медіа.")
                        return

            elif action == "prev":
                if index > 0:
                    context.user_data['moderation_index'] -= 1
                else:
                    await query.answer("Це перше медіа.")
                    return

            await self._show_current_media(update, context, user_id)

        except Exception as e:
            logger.error(f"Error in moderation action: {e}")
            await query.answer("❌ Виникла помилка при обробці дії.")

    async def _process_moderation(self, 
                                media_id: str, 
                                action: str, 
                                moderator_id: str,
                                reason: Optional[str] = None) -> bool:
        """Обробка модераційної дії"""
        try:
            if action == "approve":
                result = await self.hero_service.approve_media(
                    media_id=media_id,
                    moderator_id=moderator_id
                )
            else:
                result = await self.hero_service.reject_media(
                    media_id=media_id,
                    moderator_id=moderator_id,
                    reason=reason
                )
            return result
        except Exception as e:
            logger.error(f"Error processing moderation action: {e}")
            return False

    async def _show_current_media(self, update: Update, context: ContextTypes.DEFAULT_TYPE, user_id: str):
        """Показ поточного медіа для модерації"""
        try:
            index = context.user_data.get('moderation_index', 0)
            media_list = self.pending_media.get(user_id, [])

            if not media_list:
                if update.callback_query:
                    await update.callback_query.edit_message_text("Список медіа порожній.")
                else:
                    await update.message.reply_text("Список медіа порожній.")
                return

            media = media_list[index]

            # Створюємо клавіатуру для модерації
            keyboard = [
                [
                    InlineKeyboardButton("✅ Схвалити", callback_data="mod_approve"),
                    InlineKeyboardButton("❌ Відхилити", callback_data="mod_reject"),
                ],
                [
                    InlineKeyboardButton("⬅️", callback_data="mod_prev"),
                    InlineKeyboardButton(f"{index + 1}/{len(media_list)}", 
                                       callback_data="mod_count"),
                    InlineKeyboardButton("➡️", callback_data="mod_next"),
                ],
            ]

            reply_markup = InlineKeyboardMarkup(keyboard)

            caption = (
                f"📸 Автор: @{media.author_nickname}\n"
                f"🗓 Додано: {media.created_at.strftime('%d.%m.%Y %H:%M')}\n"
                f"📝 Тип: {media.media_type}\n"
                f"🆔 Media ID: {media.id}\n\n"
                f"ℹ️ Метадані:\n{self._format_metadata(media.metadata)}"
            )

            try:
                if update.callback_query:
                    await update.callback_query.edit_message_media(
                        media=InputMediaPhoto(
                            media=media.url,
                            caption=caption
                        ),
                        reply_markup=reply_markup
                    )
                else:
                    await context.bot.send_photo(
                        chat_id=update.effective_chat.id,
                        photo=media.url,
                        caption=caption,
                        reply_markup=reply_markup
                    )
            except TelegramError as e:
                logger.error(f"Telegram error showing media: {e}")
                # Спробуємо показати наступне медіа
                media_list.pop(index)
                await self._show_current_media(update, context, user_id)

        except Exception as e:
            logger.error(f"Error showing media: {e}")
            if update.callback_query:
                await update.callback_query.answer("❌ Виникла помилка при показі медіа.")

    def _format_metadata(self, metadata: Dict) -> str:
        """Форматування метаданих для відображення"""
        return '\n'.join(f"- {k}: {v}" for k, v in metadata.items())

    def get_handlers(self):
        """Отримання обробників для реєстрації"""
        return [
            CommandHandler('moderation', self.moderation_panel),
            CallbackQueryHandler(self.handle_moderation_action, pattern='^mod_'),
            CallbackQueryHandler(self.handle_moderation_action, pattern='^reason_'),
        ]

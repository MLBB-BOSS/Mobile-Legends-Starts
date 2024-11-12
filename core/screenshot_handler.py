# core/screenshot_handler.py

import logging
from telegram import Update
from telegram.ext import ContextTypes
from services.s3 import upload_file_to_s3
from models.contribution import Contribution
from config.settings import AWS_S3_BUCKET_NAME

logger = logging.getLogger(__name__)

async def handle_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        photo = update.message.photo[-1]  # Отримання найвищої якості фото
        file = await context.bot.get_file(photo.file_id)
        file_path = f"screenshots/{user.id}_{photo.file_id}.jpg"
        await file.download_to_drive(file_path)

        # Завантаження файлу до S3
        object_name = f"{user.id}/{photo.file_id}.jpg"
        s3_url = upload_file_to_s3(file_path, object_name)

        if not s3_url:
            await update.message.reply_text("Виникла помилка при завантаженні скріншоту до хмарного сховища.")
            return

        # Збереження інформації до бази даних
        contribution = Contribution(
            user_id=user.id,
            contribution_type='screenshot',
            points=10,  # Наприклад, 10 балів за скріншот
            screenshot_url=s3_url
        )
        contribution.save()  # Метод для збереження в базі даних

        await update.message.reply_text("Скріншот успішно завантажено! Ви отримали 10 балів та бейдж 'Novice'.")
        logger.info(f"User {user.username or user.id} uploaded a screenshot.")
    except Exception as e:
        logger.error(f"Error in handle_screenshot: {e}")
        await update.message.reply_text("Виникла помилка при завантаженні скріншоту.")

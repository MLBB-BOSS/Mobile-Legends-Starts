# core/screenshot_handler.py

import logging
from telegram import Update
from telegram.ext import CallbackContext
from models.contribution import Contribution
from models.contributor import Contributor
from services.database import SessionLocal
from utils.achievements_manager import update_achievements

logger = logging.getLogger(__name__)

def handle_screenshot(update: Update, context: CallbackContext):
    try:
        if update.message.photo:
            photo_file = update.message.photo[-1].get_file()
            file_path = os.path.join('screenshots', f"{update.message.from_user.id}_{photo_file.file_id}.jpg")
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            photo_file.download(file_path)
            update.message.reply_text('Скріншот успішно завантажено! +5 балів')
            logger.info(f"Screenshot saved to {file_path}")

            db = SessionLocal()
            contributor = db.query(Contributor).filter_by(telegram_id=update.message.from_user.id).first()

            if not contributor:
                contributor = Contributor(
                    telegram_id=update.message.from_user.id,
                    username=update.message.from_user.username
                )
                db.add(contributor)
                db.commit()
                db.refresh(contributor)
                logger.info(f"Created new contributor: {contributor.username}")

            # Додавання внеску
            contribution = Contribution(
                contributor_id=contributor.id,
                contribution_type="skin",
                description="Завантаження скріншоту скіна"
            )
            db.add(contribution)

            # Додавання балів за внесок
            contributor.points += 5
            logger.info(f"Contributor {contributor.username} earned 5 points")

            # Оновлення бейджів та рівнів
            update_achievements(db, contributor)

            db.commit()
            db.refresh(contributor)
            logger.info(f"Contributor {contributor.username} now has {contributor.points} points and level {contributor.level}")

            update.message.reply_text(f"Ваші бали: {contributor.points}\nРівень: {contributor.level}")

        else:
            update.message.reply_text('Будь ласка, надішліть скріншот.')
            logger.warning("Received non-photo message for screenshot")
    except Exception as e:
        logger.error(f"Error in handle_screenshot: {e}")
        update.message.reply_text("Виникла помилка при обробці скріншоту.")

from telegram import Update
from telegram.ext import ContextTypes
from services.screenshot_service import ScreenshotService
from sqlalchemy.ext.asyncio import AsyncSession

async def handle_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE, session: AsyncSession):
    """Обробляє отримані скріншоти"""
    # Перевіряємо, чи є в повідомленні фото
    if not update.message.photo:
        await update.message.reply_text("Будь ласка, надішліть скріншот.")
        return

    # Отримуємо найбільшу версію фото
    photo = update.message.photo[-1]
    user_id = update.effective_user.id

    # Створюємо сервіс та зберігаємо скріншот
    screenshot_service = ScreenshotService(session)
    screenshot = await screenshot_service.save_screenshot(
        user_id=user_id,
        file_id=photo.file_id
    )

    await update.message.reply_text(
        "Скріншот успішно збережено! "
        "Використайте /screenshots щоб переглянути всі ваші скріншоти."
    )

async def list_screenshots(update: Update, context: ContextTypes.DEFAULT_TYPE, session: AsyncSession):
    """Показує список скріншотів користувача"""
    user_id = update.effective_user.id
    screenshot_service = ScreenshotService(session)
    screenshots = await screenshot_service.get_user_screenshots(user_id)

    if not screenshots:
        await update.message.reply_text("У вас поки немає збережених скріншотів.")
        return

    message = "Ваші збережені скріншоти:\n\n"
    for idx, screenshot in enumerate(screenshots, 1):
        message += f"{idx}. Створено: {screenshot.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
        if screenshot.hero_name:
            message += f"   Герой: {screenshot.hero_name}\n"

    await update.message.reply_text(message)

from aiogram import Router, types
from services.message_service import send_message, delete_message, edit_message

router = Router()

@router.callback_query(text="send_message")
async def send_new_message(callback: types.CallbackQuery):
    """
    Надсилання нового повідомлення.
    """
    await callback.message.edit_text("Напишіть текст повідомлення, яке потрібно надіслати:")
    await callback.answer()
    
    # Очікуємо текст повідомлення від користувача
    @router.message()
    async def handle_new_message(message: types.Message):
        response = await send_message(message.text)
        await message.answer(f"✅ Повідомлення надіслано:\n{response}")

@router.callback_query(text="delete_message")
async def delete_existing_message(callback: types.CallbackQuery):
    """
    Видалення повідомлення.
    """
    await callback.message.edit_text("Вкажіть ID повідомлення для видалення:")
    await callback.answer()

    @router.message()
    async def handle_delete_message(message: types.Message):
        success = await delete_message(message.text)
        if success:
            await message.answer(f"✅ Повідомлення з ID {message.text} видалено.")
        else:
            await message.answer("❌ Помилка: повідомлення не знайдено.")

@router.callback_query(text="edit_message")
async def edit_existing_message(callback: types.CallbackQuery):
    """
    Редагування повідомлення.
    """
    await callback.message.edit_text("Вкажіть ID повідомлення для редагування:")
    await callback.answer()

    @router.message()
    async def handle_edit_message_id(message: types.Message):
        message_id = message.text
        await message.answer("Напишіть новий текст для повідомлення:")

        @router.message()
        async def handle_new_message_text(new_message: types.Message):
            success = await edit_message(message_id, new_message.text)
            if success:
                await new_message.answer(f"✅ Повідомлення з ID {message_id} оновлено.")
            else:
                await new_message.answer("❌ Помилка: повідомлення не знайдено.")

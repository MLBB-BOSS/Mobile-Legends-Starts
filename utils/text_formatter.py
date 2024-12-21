class MessageFormatter:
    @staticmethod
    async def update_menu_message(message, title, description, keyboard):
        await message.edit_text(f"{title}\n\n{description}", reply_markup=keyboard)

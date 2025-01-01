# handlers/some_handler.py
from utils.message_utils import MessageManager

class SomeHandler:
    def __init__(self, bot: Bot):
        self.message_manager = MessageManager(bot)
        
    async def handle_something(self, message: Message):
        # Using message manager
        result = await self.message_manager.send_or_edit(
            chat_id=message.chat.id,
            text="Some text",
            keyboard=some_keyboard
        )
        
        if result:
            # Save message_id for future edits
            await state.update_data(last_message_id=result.message_id)

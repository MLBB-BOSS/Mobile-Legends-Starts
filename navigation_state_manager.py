# navigation_state_manager.py
from aiogram.fsm.context import FSMContext
from interface_messages import InterfaceMessages

class NavigationStateManager:
    """Менеджер станів навігації."""
    
    def __init__(self, state: FSMContext):
        self.state = state
        self.messages = InterfaceMessages()

    async def load_state(self) -> None:
        """Завантаження даних стану."""
        data = await self.state.get_data()
        self.messages.bot_message_id = data.get('bot_message_id')
        self.messages.interactive_message_id = data.get('interactive_message_id')
        self.messages.last_text = data.get('last_text', '')
        self.messages.last_keyboard = data.get('last_keyboard')

    async def save_state(self) -> None:
        """Збереження даних стану."""
        await self.state.update_data(
            bot_message_id=self.messages.bot_message_id,
            interactive_message_id=self.messages.interactive_message_id,
            last_text=self.messages.last_text,
            last_keyboard=self.messages.last_keyboard
        )

    async def transition_to(self, new_state: MenuStates) -> None:
        """Перехід до нового стану."""
        await self.save_state()
        await self.state.set_state(new_state)

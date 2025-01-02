# utils/context.py
class BotContext:
    def __init__(self, bot: Bot, state: FSMContext):
        self.bot = bot
        self.state = state
        self._data = {}

    async def load_data(self):
        self._data = await self.state.get_data()

    async def save_data(self):
        await self.state.set_data(self._data)

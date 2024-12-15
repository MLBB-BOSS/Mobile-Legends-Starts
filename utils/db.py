from aiogram.dispatcher.middlewares import BaseMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

class DBSessionMiddleware(BaseMiddleware):
    def __init__(self, db_session: AsyncSession):
        super().__init__()
        self.db_session = db_session

    async def on_pre_process_update(self, update, data):
        # Передати db в обробники
        data['db'] = self.db_session
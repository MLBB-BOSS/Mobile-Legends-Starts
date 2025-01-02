from typing import Any, Awaitable, Callable, Dict
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery, Update
from sqlalchemy.ext.asyncio import AsyncSession

class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, session_pool):
        self.session_pool = session_pool
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[Update, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        async with self.session_pool() as session:
            data['db'] = session
            try:
                return await handler(event, data)
            except Exception as e:
                # Отримуємо chat_id з події
                chat_id = None
                if isinstance(event, Message):
                    chat_id = event.chat.id
                elif isinstance(event, CallbackQuery):
                    chat_id = event.message.chat.id
                
                logger.error(f"Database Middleware Error for chat_id {chat_id}: {e}")
                if 'bot' in data and chat_id:
                    await handle_error(
                        bot=data['bot'],
                        chat_id=chat_id,
                        error_message=GENERIC_ERROR_MESSAGE_TEXT,
                        logger=logger
                    )
            finally:
                await session.close()

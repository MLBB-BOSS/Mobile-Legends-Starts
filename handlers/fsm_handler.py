#handlers/fsm_handler.py
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from typing import Optional, Any

class AsyncFSMHandler:
    """Базовий клас для асинхронної обробки станів"""
    
    def __init__(self, state: FSMContext):
        self.state = state
        
    async def get_current_state(self) -> Optional[State]:
        """Отримати поточний стан"""
        return await self.state.get_state()
    
    async def set_state(self, state: State):
        """Встановити новий стан"""
        await self.state.set_state(state)
        
    async def finish(self):
        """Завершити поточний стан"""
        await self.state.clear()
        
    async def update_data(self, **kwargs):
        """Оновити дані стану"""
        await self.state.update_data(**kwargs)
        
    async def get_data(self) -> dict:
        """Отримати дані стану"""
        return await self.state.get_data()
        
    async def get_data_value(self, key: str, default: Any = None) -> Any:
        """Отримати конкретне значення зі стану"""
        data = await self.get_data()
        return data.get(key, default)

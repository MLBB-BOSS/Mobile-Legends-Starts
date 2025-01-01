# handlers/fsm_handler.py
from typing import Optional
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from logging import getLogger

class FSMContextManager:
    """Manager for FSM context operations"""
    
    def __init__(self, state: FSMContext):
        self._state = state
        self.logger = getLogger("handlers.fsm")

    async def get_current_state(self) -> Optional[str]:
        """Get current state name"""
        try:
            return await self._state.get_state()
        except Exception as e:
            self.logger.error(f"Error getting state: {e}")
            return None

    async def set_state(self, state: State) -> None:
        """Set new state"""
        try:
            await self._state.set_state(state)
        except Exception as e:
            self.logger.error(f"Error setting state: {e}")
            raise

    async def finish(self) -> None:
        """Finish current state"""
        try:
            await self._state.clear()
        except Exception as e:
            self.logger.error(f"Error finishing state: {e}")
            raise

# Make sure to export FSMContextManager
__all__ = ['FSMContextManager']

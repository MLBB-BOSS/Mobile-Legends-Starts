# handlers/fsm_handler.py
from typing import Optional
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from logging import getLogger

class FSMContextManager:
    """Manager for FSM context operations"""
    
    def __init__(self, state: FSMContext):
        self._state = state
        self.logger = getLogger(__name__)

    async def get_current_state(self) -> Optional[str]:
        """
        Get current state name
        
        Returns:
            Optional[str]: Current state name or None
        """
        try:
            current_state = await self._state.get_state()
            # current_state вже є строкою або None
            return current_state
            
        except Exception as e:
            self.logger.error(f"Error getting current state: {e}")
            return None

    async def set_state(self, state: State) -> None:
        """
        Set new state
        
        Args:
            state: New state to set
        """
        try:
            await self._state.set_state(state)
        except Exception as e:
            self.logger.error(f"Error setting state: {e}")
            raise

    async def update_data(self, **kwargs) -> None:
        """
        Update state data
        
        Args:
            **kwargs: Data to update
        """
        try:
            await self._state.update_data(**kwargs)
        except Exception as e:
            self.logger.error(f"Error updating state data: {e}")
            raise

    async def get_data(self) -> dict:
        """
        Get current state data
        
        Returns:
            dict: Current state data
        """
        try:
            return await self._state.get_data()
        except Exception as e:
            self.logger.error(f"Error getting state data: {e}")
            return {}

    async def clear(self) -> None:
        """Clear current state and data"""
        try:
            await self._state.clear()
        except Exception as e:
            self.logger.error(f"Error clearing state: {e}")
            raise

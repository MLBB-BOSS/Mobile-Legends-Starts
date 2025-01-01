from typing import Any, Dict, Optional
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State

class AsyncFSMHandler:
    """Async FSM context handler"""
    
    def __init__(self, state: FSMContext) -> None:
        self._state = state

    async def get_current_state(self) -> Optional[str]:
        """
        Get current state
        
        Returns:
            Optional[str]: Current state or None
        """
        state = await self._state.get_state()
        return state.state if state else None

    async def set_state(self, state: State) -> None:
        """
        Set new state
        
        Args:
            state: New state to set
        """
        await self._state.set_state(state)

    async def update_data(self, **kwargs: Any) -> None:
        """
        Update state data
        
        Args:
            **kwargs: Key-value pairs to update
        """
        await self._state.update_data(**kwargs)

    async def get_data(self) -> Dict[str, Any]:
        """
        Get state data
        
        Returns:
            Dict[str, Any]: Current state data
        """
        return await self._state.get_data()

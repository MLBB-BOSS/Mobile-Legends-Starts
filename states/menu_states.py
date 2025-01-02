from aiogram.fsm.state import State, StatesGroup

class ProfileState(StatesGroup):
    # Profile related states
    view = State()
    edit = State()
    settings = State()
    # Add other profile-related states as needed

class MenuStates(StatesGroup):
    # Menu related states
    main = State()
    settings = State()
    tournaments = State()
    screenshots = State()

# Make sure to include all states you're exporting
__all__ = ['ProfileState', 'MenuStates']

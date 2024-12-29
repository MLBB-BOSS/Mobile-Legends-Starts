from .base_handler import BaseHandler
from states.state_groups import NavigationState, MainMenuState
from keyboards.menus import get_navigation_menu
from keyboards.inline import get_generic_inline_keyboard
from texts.navigation import NAVIGATION_MENU_TEXT, NAVIGATION_INTERACTIVE_TEXT

class NavigationHandler(BaseHandler):
    def register_handlers(self):
        """Реєстрація обробників навігаційного меню"""
        self.router.message(MainMenuState.main)(self.handle_navigation_transition)
        self.router.message(NavigationState.main)(self.handle_navigation_menu)

    async def handle_navigation_transition(self, message: Message, state: FSMContext):
        """Обробка переходу до навігаційного меню"""
        if message.text == "🧭 Навігація":
            await self.handle_transition(
                message=message,
                state=state,
                new_state=NavigationState.main,
                control_text=NAVIGATION_MENU_TEXT,
                control_markup=get_navigation_menu(),
                screen_text=NAVIGATION_INTERACTIVE_TEXT,
                screen_markup=get_generic_inline_keyboard()
            )

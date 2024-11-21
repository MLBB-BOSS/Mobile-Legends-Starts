from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

class BaseKeyboard:
    """Base class for all keyboards"""
    
    def create_reply_markup(
        self,
        keyboard: list[list[str]],
        resize_keyboard: bool = True,
        one_time_keyboard: bool = False
    ) -> ReplyKeyboardMarkup:
        """
        Creates a reply keyboard markup from a list of button texts
        
        Args:
            keyboard: List of lists of button texts
            resize_keyboard: Whether to resize the keyboard
            one_time_keyboard: Whether to hide keyboard after first use
        """
        markup = ReplyKeyboardMarkup(
            resize_keyboard=resize_keyboard,
            one_time_keyboard=one_time_keyboard
        )
        
        for row in keyboard:
            markup.row(*[KeyboardButton(text=button) for button in row])
            
        return markup

    def create_inline_markup(self, buttons: list[list[tuple[str, str]]]) -> InlineKeyboardMarkup:
        """
        Creates an inline keyboard markup from a list of button tuples
        
        Args:
            buttons: List of lists of (text, callback_data) tuples
        """
        markup = InlineKeyboardMarkup()
        
        for row in buttons:
            markup.row(*[InlineKeyboardButton(
                text=button[0],
                callback_data=button[1]
            ) for button in row])
            
        return markup

    def create_url_markup(self, buttons: list[list[tuple[str, str]]]) -> InlineKeyboardMarkup:
        """
        Creates an inline keyboard markup with URL buttons
        
        Args:
            buttons: List of lists of (text, url) tuples
        """
        markup = InlineKeyboardMarkup()
        
        for row in buttons:
            markup.row(*[InlineKeyboardButton(
                text=button[0],
                url=button[1]
            ) for button in row])
            
        return markup

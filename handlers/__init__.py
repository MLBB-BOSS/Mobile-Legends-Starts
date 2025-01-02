# handlers/__init__.py
from aiogram import Dispatcher  # Add this import at the top

def setup_handlers(dp: Dispatcher):
    from .base import base_handlers
    from .features import feature_handlers
    
    all_handlers = (
        *base_handlers,
        *feature_handlers
    )
    
    for handler in all_handlers:
        dp.register_message_handler(handler)

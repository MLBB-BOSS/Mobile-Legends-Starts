# handlers/__init__.py
from aiogram import Dispatcher
from .base import base_handlers
from .features import feature_handlers

def setup_handlers(dp: Dispatcher):
    all_handlers = (
        *base_handlers,
        *feature_handlers
    )
    
    for handler in all_handlers:
        dp.register_message_handler(handler)

from .base import router as base_router

def setup_handlers(dp):
    """
    Реєстрація обробників.
    """
    dp.include_router(base_router)

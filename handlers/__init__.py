from aiogram import Dispatcher
from .base import router as base_router
from .missing_handlers import router as missing_handlers_router

def setup_handlers(dp: Dispatcher):
    routers = [base_router, missing_handlers_router]

    for router in routers:
        if router not in dp.routers:
            dp.include_router(router)

# __init__.py
def setup_handlers(dp: Dispatcher):
    from .profile import profile_router
    from .team import team_router
    from .tournaments import tournament_router
    
    routers = [
        profile_router,
        team_router,
        tournament_router
    ]
    
    for router in routers:
        dp.include_router(router)

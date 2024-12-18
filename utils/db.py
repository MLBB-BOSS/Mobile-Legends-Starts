# utils/db.py

async def get_user_profile(session: AsyncSession, user_id: int):
    """
    Отримання профілю користувача з бази даних.
    """
    try:
        result = await session.execute(
            select(models.user.User, models.user_stats.UserStats).where(models.user.User.telegram_id == user_id).join(models.user_stats.UserStats)
        )
        user, stats = result.first()
        if user and stats:
            return {
                "username": user.username,
                "level": stats.level,
                "rating": stats.rating,
                "achievements_count": stats.achievements_count,
                "screenshots_count": stats.screenshots_count,
                "missions_count": stats.missions_count,
                "quizzes_count": stats.quizzes_count,
                "total_matches": stats.total_matches,
                "total_wins": stats.total_wins,
                "total_losses": stats.total_losses,
                "tournament_participations": stats.tournament_participations,
                "badges_count": stats.badges_count,
                "last_update": stats.last_update,
            }
        return None
    except Exception as e:
        logger.error(f"Error fetching user profile for user_id {user_id}: {e}")
        return None
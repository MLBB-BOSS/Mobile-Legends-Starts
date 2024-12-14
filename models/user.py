# services/user_service.py
async def get_user_rating_history(db: AsyncSession, user_id: int) -> list[int]:
    try:
        stmt = select(RatingHistory).where(RatingHistory.user_id == user_id).order_by(RatingHistory.timestamp)
        result = await db.execute(stmt)
        history = result.scalars().all()
        return [record.rating for record in history]
    except SQLAlchemyError as e:
        logger.error(f"Error fetching rating history for user_id={user_id}: {e}")
        return []
from sqlalchemy.exc import SQLAlchemyError
from bot.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession


async def create_user(session: AsyncSession, full_name: str, email: str) -> User:
    user = User(full_name=full_name, email=email)
    session.add(user)
    try:
        await session.commit()
    except SQLAlchemyError:
        await session.rollback()
        raise
    return user


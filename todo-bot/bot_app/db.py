from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from bot.config import config
from sqlalchemy.ext.declarative import declarative_base
from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject


# Создаем движок для работы с базой данных
engine = create_async_engine(f"postgresql+asyncpg://{config.POSTGRES_USER}:{config.POSTGRES_PASSWORD}@{config.POSTGRES_URL}:{config.POSTGRES_PORT}/{config.POSTGRES_DB}", echo=True)

# Создаем фабрику асинхронных сессий
async_session = sessionmaker(
    engine,
    expire_on_commit=False,  # Не сбрасывать данные в объектах после фиксации
    class_=AsyncSession
)

# Базовый класс для ORM-моделей
Base = declarative_base()




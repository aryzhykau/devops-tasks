from logging.config import fileConfig
import os

from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import pool
from db import Base
from bot.models.user import User # Здесь подключаются метаданные вашего приложения

# Загрузка переменных окружения из формы .env
from dotenv import load_dotenv

load_dotenv(".env")

# Чтение URL базы данных из .env (или установка значения по умолчанию)
POSTGRES_URL = os.getenv("POSTGRES_URL", "localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "<PASSWORD>")
POSTGRES_DB = os.getenv("POSTGRES_DB", "postgres")
print(POSTGRES_URL)
print(POSTGRES_DB)
print(POSTGRES_USER)
print(POSTGRES_PASSWORD)
print(POSTGRES_PORT)
# This is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata to be used in migrations
target_metadata = Base.metadata


def run_migrations_offline():
    """
    Запуск миграций в режиме 'offline' (без подключения к базе данных).
    """
    context.configure(
        url=f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_URL}:{POSTGRES_PORT}/{POSTGRES_DB}",
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """
    Запуск миграций в режиме 'online' (с подключением к базе данных).
    """
    connectable = create_async_engine(
        f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_URL}:{POSTGRES_PORT}/{POSTGRES_DB}",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


def do_run_migrations(connection):
    """
    Привязка подключения к Alembic.
    """
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )

    with context.begin_transaction():
        context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    import asyncio

    asyncio.run(run_migrations_online())

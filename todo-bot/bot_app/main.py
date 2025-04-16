from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.fsm.storage.memory import MemoryStorage
from db import  async_session
from bot.middlewares.db_middleware import DatabaseSessionMiddleware
from bot.middlewares.state_middleware import PydanticStateMiddleware
from bot.schemas.user import UserStateModel
from bot.handlers.start import user_creation_router
from bot.config import config
import asyncio




# Создаем объекты бота и диспетчера
bot = Bot(token=config.BOT_TOKEN)
if config.REDIS_ENABLED and config.REDIS_URL:
    dp = Dispatcher(storage=RedisStorage.from_url(config.REDIS_URL))
    print("Redis connected")
else:
    dp = Dispatcher(storage=MemoryStorage())

dp.update.middleware(DatabaseSessionMiddleware(async_session))
dp.update.middleware(PydanticStateMiddleware(UserStateModel, state_key="user_state"))
# Простейший обработчик команды /start
dp.include_router(user_creation_router)


async def main():

    # Запускаем диспетчер
    await dp.start_polling(bot)


if __name__ == "__main__":

    asyncio.run(main())

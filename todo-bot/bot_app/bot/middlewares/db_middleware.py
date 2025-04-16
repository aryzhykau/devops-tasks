from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class DatabaseSessionMiddleware(BaseMiddleware):
    def __init__(self, async_sessionmaker):
        super().__init__()
        self.async_sessionmaker = async_sessionmaker

    async def __call__(self, handler, event: TelegramObject, data: dict):
        # Открываем сессию
        async with self.async_sessionmaker() as session:
            try:
                # Передаем сессию в `data`
                data['session'] = session
                # Выполняем обработчик
                return await handler(event, data)
            except Exception:
                # Если произошла ошибка, откатываем транзакцию
                await session.rollback()
                raise  # Пробрасываем исключение дальше
            finally:
                # Явно закрываем сессию (необязательно, так как async with это делает)
                await session.close()

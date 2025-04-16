from aiogram.dispatcher.middlewares.base import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram.fsm.context import FSMContext
from pydantic import BaseModel


class PydanticStateMiddleware(BaseMiddleware):
    def __init__(self, model: BaseModel, state_key: str = "user_state"):
        """
        Middleware для автоматической работы с Pydantic-моделью состояния.

        :param model: класс Pydantic модели
        :param state_key: ключ, под которым состояние будет храниться в FSM
        """
        super().__init__()
        self.model = model
        self.state_key = state_key

    async def __call__(self, handler, event: TelegramObject, data: dict):
        # Получаем FSMContext
        state: FSMContext = data.get('state')
        if not state:
            return await handler(event, data)

        # Загружаем данные из состояния и создаем Pydantic модель
        state_data = await state.get_data()
        model_data = state_data.get(self.state_key, {})
        pydantic_instance = self.model.model_validate(model_data)

        # Передаем Pydantic модель в data
        data[self.state_key] = pydantic_instance

        # Выполняем обработчик
        result = await handler(event, data)

        # Сохраняем обновленную Pydantic модель обратно в состояние
        updated_model = data.get(self.state_key)
        if isinstance(updated_model, self.model):
            await state.update_data({self.state_key: updated_model.model_dump()})

        # Возвращаем результат обработчика
        return result





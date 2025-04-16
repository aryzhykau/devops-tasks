from aiogram import Router, F, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.filters import Command
from bot.states.states import UserCreationStates
from bot.schemas.user import UserStateModel
from bot.crud.user import create_user
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from sqlalchemy.ext.asyncio import AsyncSession

# Создаем Router
user_creation_router = Router()

@user_creation_router.message(Command(commands=["start"]))
async def start_command_handler(message: types.Message, state: FSMContext):
    await message.answer("Введите, пожалуйста, ваше имя и фамилию:")
    await state.set_state(UserCreationStates.enter_full_name)


@user_creation_router.message(UserCreationStates.enter_full_name)
async def enter_full_name(message: types.Message, user_state: UserStateModel, state: FSMContext):

    user_state.full_name = message.text

    await state.set_state(UserCreationStates.enter_email)
    await message.answer("Теперь введи email")




@user_creation_router.message(UserCreationStates.enter_email)
async def enter_full_name(message: types.Message, user_state: UserStateModel):
    try:
        email = message.text.strip()
        user_state.email = email

    # Create InlineKeyboardMarkup
        builder = InlineKeyboardBuilder()
        builder.add(
            InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_creation"),
            InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_creation")
        )

        await message.answer("Сохранить данные? Подтвердите или отмените действие:",
                             reply_markup=builder.as_markup())
    except ValueError:
        await message.answer("Неверный формат email. Попробуйте ещё раз.")


@user_creation_router.callback_query(F.data.in_({"confirm_creation", "cancel_creation"}))
async def confirm_cancel_handler(callback: types.CallbackQuery, user_state: UserStateModel, session: AsyncSession, state: FSMContext):
    if callback.data == "confirm_creation":
        await create_user(session, user_state.full_name, user_state.email)
        await callback.message.answer("Создание пользователя подтверждено!")
        await state.clear()
    elif callback.data == "cancel_creation":
        await callback.message.answer("Создание пользователя отменено. Нажмите старт еще раз")
        await state.clear()
    await callback.answer()




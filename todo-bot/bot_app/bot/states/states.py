from aiogram.fsm.state import StatesGroup, State

class UserCreationStates(StatesGroup):
    enter_username = State()
    enter_full_name = State()
    enter_email = State()
    confirm = State()


class SendImageToS3States(StatesGroup):
    waiting_for_image = State()
    ask_for_confirmation = State()
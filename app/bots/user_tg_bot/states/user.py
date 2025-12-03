from aiogram.fsm.state import State, StatesGroup


class RegisterUserStates(StatesGroup):
    get_phone_number = State()
    get_name = State()


class ProfileUserStates(StatesGroup):
    get_base_location = State()


class UserCreateOrderStates(StatesGroup):
    get_start_point = State()
    get_end_point = State()
    get_point = State()
    get_comment = State()


class UserCancelOrderStates(StatesGroup):
    get_reason = State()


class UserWithOrderStates(StatesGroup):
    editing_order = State()
    user_with_active_order = State()

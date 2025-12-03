from aiogram.fsm.state import State, StatesGroup


class DriverShiftStates(StatesGroup):
    get_translate_location = State()

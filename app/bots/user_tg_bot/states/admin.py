from aiogram.fsm.state import State, StatesGroup


class AdminCreateCityStates(StatesGroup):
    get_city_name = State()
    get_city_state = State()
    get_city_base_price = State()
    get_city_price_per_km = State()
    get_city_service_commission = State()
    get_city_polygon_coords = State()


class AdminCreateDriverStates(StatesGroup):
    get_user_id = State()
    get_driver_first_name = State()
    get_driver_last_name = State()
    get_driver_middle_name = State()
    get_driver_license = State()
    get_driver_phone_number = State()


class AdminSearchUserStates(StatesGroup):
    get_phone_number = State()
    get_user_id = State()


class AdminBlockUserStates(StatesGroup):
    get_reason = State()
    get_days = State()
    get_minutes = State()
    get_hours = State()

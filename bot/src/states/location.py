from aiogram.fsm.state import State, StatesGroup


class LocationState(StatesGroup):
    location: State = State()

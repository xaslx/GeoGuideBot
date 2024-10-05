from aiogram.fsm.state import State, StatesGroup


class AddEstablishmentState(StatesGroup):
    type_id: State = State()
    title: State = State()
    description: State = State()
    address: State = State()
    photo_url: State = State()
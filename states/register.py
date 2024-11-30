from aiogram.fsm.state import State, StatesGroup


class Register(StatesGroup):
    lang = State()
    phone = State()

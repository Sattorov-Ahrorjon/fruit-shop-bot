from aiogram.fsm.state import State, StatesGroup


class PaymentState(StatesGroup):
    pay_type = State()
    deliver_time = State()
    location = State()
    phone = State()

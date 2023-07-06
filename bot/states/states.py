from aiogram.fsm.state import State, StatesGroup

class orderStates(StatesGroup):
    shipment = State()
    number = State()
    send_order = State()
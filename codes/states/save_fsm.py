from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    name = State()
    surname = State()
    age = State()
    city = State()
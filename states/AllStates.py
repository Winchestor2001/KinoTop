from aiogram.dispatcher.filters.state import StatesGroup, State


class Adminstate(StatesGroup):
    edit_film_channel = State()
    mailing = State()
    add_channel = State()





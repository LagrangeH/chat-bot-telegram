from aiogram.dispatcher.filters.state import StatesGroup, State


class BotStates(StatesGroup):
    Weather = State()
    Convert = State()
    Poll = State()

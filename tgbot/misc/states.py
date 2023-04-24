from aiogram.dispatcher.filters.state import StatesGroup, State


class BotStates(StatesGroup):
    Weather = State()
    Poll = State()


class ConvertStates(StatesGroup):
    Convert = State()
    ConvertTo = State()
    ConvertFrom = State()

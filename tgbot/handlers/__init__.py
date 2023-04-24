from aiogram import Dispatcher

from tgbot.handlers.cat import register_cat
from tgbot.handlers.convert import register_convert
from tgbot.handlers.main import register_main, undefined_message
from tgbot.handlers.poll import register_poll
from tgbot.handlers.weather import register_weather


def register_handlers(dp: Dispatcher) -> None:
    register_main(dp)
    register_convert(dp)
    register_poll(dp)
    register_cat(dp)
    register_weather(dp)

    # Handler of undefined messages should be registered last
    dp.register_message_handler(undefined_message, state='*')

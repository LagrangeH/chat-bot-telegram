from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.misc import cute_cat
from tgbot.keyboards.inline import cities_kb


async def start_or_help_commands(message: Message) -> None:
    """
    Handles /start and /help commands
    :param message:
    :return:
    """
    await message.reply(
        "Чтобы начать, выбери команду из списка доступных\n👇",
    )


async def weather_command(message: Message) -> None:
    """
    Handles /weather command
    :param message:
    :return:
    """
    await message.reply(
        "Выберите город или напишите название любого другого города, чтобы узнать погоду",
        reply_markup=cities_kb,
    )


async def convert_command(message: Message) -> None:
    """
    Handles /convert command
    :param message:
    :return:
    """
    await message.reply(
        "Введите сумму и валюту, чтобы конвертировать валюту\n"
        "Пример: 100 usd to rub",
    )


async def cat_command(message: Message) -> None:
    """
    Handles /cat command
    :param message:
    :return:
    """
    await message.reply_photo(
        cute_cat.get_cat_picture(message.bot['config'].cat_api_key),
    )


async def poll_command(message: Message) -> None:
    """
    Handles /poll command
    :param message:
    :return:
    """
    await message.reply(
        "Введите вопрос и варианты ответа через запятую\n"
        "Пример: Какой фильм вы любите больше?, Властелин колец, Звездные войны",
    )


async def cancel_command(message: Message) -> None:
    """
    Handles /cancel command
    :param message:
    :return:
    """
    await message.reply(
        "Отменено",
    )


async def undefined_message(message: Message) -> None:
    """
    Handles messages not caught by other handlers
    :param message:
    :return:
    """
    await message.reply(
        "Я не знаю такой команды, попробуй еще раз или выбери команду из списка\n👇",
    )


def register_user(dp: Dispatcher):
    dp.register_message_handler(start_or_help_commands, commands=['start', 'help'], state='*')
    dp.register_message_handler(weather_command, commands=['weather'], state='*')
    dp.register_message_handler(convert_command, commands=['convert'], state='*')
    dp.register_message_handler(cat_command, commands=['cat'], state='*')
    dp.register_message_handler(poll_command, commands=['poll'], state='*')
    dp.register_message_handler(cancel_command, commands=['cancel'], state='*')

    dp.register_message_handler(undefined_message, state='*')

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from tgbot.misc import cute_cat
from tgbot.misc.exchange_rates import get_exchange_rate
# from tgbot.keyboards.inline import cities_kb
from tgbot.misc.states import BotStates
from tgbot.misc.weather import get_weather


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
        # reply_markup=cities_kb,
    )
    await BotStates.Weather.set()


async def weather_city(message: Message, state: FSMContext) -> None:
    """
    :param message:
    :param state:
    :return:
    """
    weather = get_weather(message.text, message.bot['config'].weather_api_key)
    if weather is None:
        await message.answer(f"Город {message.text} не найден. Попробуйте еще раз")
        await state.finish()
    else:
        await message.reply(
            f"Погода в городе <b>{message.text}</b>: {weather['description']}\n"
            f"Температура: <code>{weather['temperature']}°C</code>\n"
            f"Ощущается как: <code>{weather['feels_like']}°C</code>\n"
            f"Влажность: <code>{weather['humidity']}%</code>\n"
            f"Скорость ветра: <code>{weather['wind_speed']} м/с</code>",
        )
    await state.finish()


async def convert_command(message: Message) -> None:
    """
    Handles /convert command
    :param message:
    :return:
    """
    await message.reply(
        "Введите сумму и валюту, чтобы конвертировать валюту\n"
        "Пример: 100 usd rub",
    )
    await BotStates.Convert.set()


async def convert_currency(message: Message, state: FSMContext) -> None:
    """
    Handles currency conversion
    :param message:
    :param state:
    :return:
    """
    amount, base, target = message.text.split()
    exchange_rate = get_exchange_rate(float(amount), base, target, message.bot['config'].exchange_api_key)
    if exchange_rate is None:
        await message.reply("Что-то пошло не так. Попробуйте еще раз")
    else:
        await message.reply(f"<code>{amount}</code> {base} = <code>{exchange_rate}</code> {target}")
    await state.finish()


async def cat_command(message: Message) -> None:
    """
    Handles /cat command and sends random cat picture
    :param message:
    :return:
    """
    cat = cute_cat.get_cat_picture(message.bot['config'].cat_api_key)
    if cat is None:
        await message.reply("Котиков не нашлось")
    else:
        await message.reply_photo(cat)


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


async def cancel_command(message: Message, state: FSMContext) -> None:
    """
    Handles /cancel command
    :param message:
    :param state:
    :return:
    """
    await message.reply(
        "Отменено",
    )
    await state.finish()


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
    # Cancel command handler should be registered before other handlers
    dp.register_message_handler(cancel_command, commands=['cancel'], state='*')

    dp.register_message_handler(start_or_help_commands, commands=['start', 'help'], state='*')
    dp.register_message_handler(weather_command, commands=['weather'], state='*')
    dp.register_message_handler(weather_city, state=BotStates.Weather)
    dp.register_message_handler(convert_command, commands=['convert'], state='*')
    dp.register_message_handler(convert_currency, state=BotStates.Convert)
    dp.register_message_handler(cat_command, commands=['cat'], state='*')
    dp.register_message_handler(poll_command, commands=['poll'], state='*')

    # Handler of undefined messages should be registered last
    dp.register_message_handler(undefined_message, state='*')

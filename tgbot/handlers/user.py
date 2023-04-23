from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from loguru import logger

from tgbot.keyboards import inline
from tgbot.middlewares import throttling
from tgbot.misc.cute_cat import get_cat_picture
from tgbot.misc.exchange_rates import get_exchange_rate
from tgbot.misc.states import BotStates
from tgbot.misc.weather import get_weather


async def start_or_help_commands(message: Message) -> None:
    """
    Handles /start and /help commands
    :param message:
    :return:
    """
    logger.debug("Got /start or /help command")
    await message.reply(
        f"Чтобы начать, выбери любую команду из списка или напиши ее самостоятельно"
        f"\n\n{message.bot['config'].commands}",
    )


async def weather_command(message: Message) -> None:
    """
    Handles /weather command
    :param message:
    :return:
    """
    logger.debug("Got /weather command")
    await message.reply(
        "Выберите город или напишите название любого другого города, чтобы узнать погоду",
        reply_markup=inline.cities
    )
    await BotStates.Weather.set()


@throttling.rate_limit(3, 'weather')
async def weather_city(message: Message, state: FSMContext) -> None:
    """
    Handles Weather state and sends weather info in chosen city
    :param message:
    :param state:
    :return:
    """
    logger.debug("Got city name for weather in Weather state")
    await state.finish()
    weather = get_weather(message.text, message.bot['config'].api_keys.weather)
    if weather is None:
        await message.answer(f"Город {message.text} не найден. Попробуйте еще раз")
        return

    await message.reply(
        f"Погода в городе <b>{message.text}</b>: {weather['description']}\n"
        f"Температура: <code>{weather['temperature']}°C</code>\n"
        f"Ощущается как: <code>{weather['feels_like']}°C</code>\n"
        f"Влажность: <code>{weather['humidity']}%</code>\n"
        f"Скорость ветра: <code>{weather['wind_speed']} м/с</code>",
    )


@throttling.rate_limit(3, 'weather')
async def weather_city_callback(query: CallbackQuery, state: FSMContext) -> None:
    logger.debug("Got city name in callback query")
    await state.finish()
    # await query.bot.answer_inline_query()
    weather = get_weather(query.data.split(':')[1], query.bot['config'].api_keys.weather)
    await query.bot.answer_callback_query(query.id)
    await query.bot.send_message(
        query.from_user.id,
        f"Погода в городе <b>{query.data.split(':')[1]}</b>: {weather['description']}\n"
        f"Температура: <code>{weather['temperature']}°C</code>\n"
        f"Ощущается как: <code>{weather['feels_like']}°C</code>\n"
        f"Влажность: <code>{weather['humidity']}%</code>\n"
        f"Скорость ветра: <code>{weather['wind_speed']} м/с</code>",
    )


async def convert_command(message: Message) -> None:
    """
    Handles /convert command
    :param message:
    :return:
    """
    logger.debug("Got /convert command")
    await message.reply(
        "Введите сумму и валюту, чтобы конвертировать валюту\n"
        "Пример: 100 usd rub",
    )
    await BotStates.Convert.set()


@throttling.rate_limit(3, 'convert')
async def convert_currency(message: Message, state: FSMContext) -> None:
    """
    Handles Convert state and sends converted currency
    :param message:
    :param state:
    :return:
    """
    logger.debug("Got currency for conversion in Convert state")

    amount, base, target = message.text.split()
    if not amount.isdigit():
        await message.reply("Сумма должна быть целым числом. Попробуйте еще раз")
        return

    exchange_rate = get_exchange_rate(float(amount), base, target, message.bot['config'].api_keys.convert)

    if exchange_rate is None:
        await message.reply("Что-то пошло не так. Попробуйте еще раз")
    else:
        await message.reply(f"<code>{amount}</code> {base} = <code>{exchange_rate}</code> {target}")
    await state.finish()


@throttling.rate_limit(2, 'cat')
async def cat_command(message: Message) -> None:
    """
    Handles /cat command and sends random cat picture
    :param message:
    :return:
    """
    logger.debug("Got /cat command")
    cat = get_cat_picture(message.bot['config'].api_keys.cat)
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
    logger.debug("Got /poll command")
    await message.reply(
        "В ответ на это сообщение введите вопрос и варианты ответа через запятую\n"
        "Пример: Какой фильм вы любите больше?, Властелин колец, Звездные войны",
    )
    await BotStates.Poll.set()


async def poll_creation(message: Message, state: FSMContext) -> None:
    """
    Handles Poll state and sends poll with given question and options
    :param message:
    :param state:
    :return:
    """
    logger.debug("Got question and options for poll in Poll state")
    question, *options = [s for s in message.text.split(',') if s]
    logger.debug(f"Question: {question}, Options: {options}")
    if len(options) < 2 or not all(options):
        await message.reply("Нужно ввести вопрос и минимум 2 варианта ответа")
    else:
        await message.answer_poll(
            question,
            options,
            is_anonymous=False,
            allows_multiple_answers=True,
        )
    await state.finish()


async def cancel_command(message: Message, state: FSMContext) -> None:
    """
    Handles /cancel command
    :param message:
    :param state:
    :return:
    """
    logger.debug("Got /cancel command")
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
    logger.debug("Got undefined message")
    await message.reply(
        f"Я не знаю такой команды, попробуй еще раз или выбери команду из списка"
        f"\n\n{message.bot['config'].commands}",
    )


def register_user(dp: Dispatcher) -> None:
    # Cancel command handler should be registered before other handlers
    dp.register_message_handler(cancel_command, commands=['cancel'], state='*')

    dp.register_message_handler(start_or_help_commands, commands=['start', 'help'], state='*')
    dp.register_message_handler(weather_command, commands=['weather'], state='*')
    dp.register_message_handler(weather_city, state=BotStates.Weather)
    dp.register_message_handler(convert_command, commands=['convert'], state='*')
    dp.register_message_handler(convert_currency, state=BotStates.Convert)
    dp.register_message_handler(cat_command, commands=['cat'], state='*')
    dp.register_message_handler(poll_command, commands=['poll'], state='*')
    dp.register_message_handler(poll_creation, state=BotStates.Poll)

    dp.register_callback_query_handler(weather_city_callback, lambda c: c.data.startswith('city'), state='*')

    # Handler of undefined messages should be registered last
    dp.register_message_handler(undefined_message, state='*')

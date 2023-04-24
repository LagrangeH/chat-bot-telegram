from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery
from loguru import logger

from tgbot.keyboards import inline
from tgbot.middlewares import throttling
from tgbot.misc.states import BotStates
from tgbot.misc.weather import get_weather


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


def register_weather(dp: Dispatcher) -> None:
    dp.register_message_handler(weather_command, commands=['weather'], state='*')
    dp.register_message_handler(weather_city, state=BotStates.Weather)
    dp.register_callback_query_handler(weather_city_callback, lambda c: c.data.startswith('city'), state='*')

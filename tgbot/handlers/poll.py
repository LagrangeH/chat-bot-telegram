from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from loguru import logger

from tgbot.misc.states import BotStates


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


def register_poll(dp: Dispatcher) -> None:
    dp.register_message_handler(poll_command, commands=['poll'], state='*')
    dp.register_message_handler(poll_creation, state=BotStates.Poll)

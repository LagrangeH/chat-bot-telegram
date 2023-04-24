from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message
from loguru import logger


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


def register_main(dp: Dispatcher) -> None:
    # Cancel command handler should be registered before other handlers
    dp.register_message_handler(cancel_command, commands=['cancel'], state='*')

    dp.register_message_handler(start_or_help_commands, commands=['start', 'help'], state='*')

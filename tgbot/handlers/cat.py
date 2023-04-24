from aiogram import Dispatcher
from aiogram.types import Message
from loguru import logger

from tgbot.middlewares import throttling
from tgbot.misc.cute_cat import get_cat_picture


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


def register_cat(dp: Dispatcher) -> None:
    dp.register_message_handler(cat_command, commands=['cat'], state='*')

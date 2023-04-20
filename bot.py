import asyncio
import sys

from aiogram.types import BotCommand
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from loguru import logger

from tgbot.config import load_config
from tgbot.handlers.user import register_user


def register_all_handlers(dp):
    register_user(dp)


async def main():
    config = load_config(".env")

    logger.remove()
    logger.add(
        sys.stdout,
        level="DEBUG" if config.debug else "INFO",
        colorize=True,
        serialize=False,
        backtrace=config.debug,
        diagnose=config.debug,
        enqueue=True,
        catch=True,
    )

    logger.debug("Configuring bot")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    register_all_handlers(dp)

    await bot.set_my_commands([
        BotCommand('weather', 'Узнать погоду'),
        BotCommand('convert', 'Конвертировать валюту'),
        BotCommand('cat', 'Случайная картинка с котиком'),
        BotCommand('poll', 'Создать опрос'),
        BotCommand('cancel', 'Отменить текущую команду'),
    ])

    bot['config'].commands = '\n'.join([f"/{command[1]} - {descr[1]}"
                                        for command, descr in await bot.get_my_commands()])

    session = await bot.get_session()

    logger.info("Bot started")

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")

import asyncio
import sys

import aiogram
from loguru import logger

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot.config import load_config
from tgbot.handlers.user import register_user
from tgbot.middlewares.environment import EnvironmentMiddleware


def register_all_middlewares(dp, config):
    dp.setup_middleware(EnvironmentMiddleware(config=config))


# def register_all_filters(dp):
#     dp.filters_factory.bind(AdminFilter)


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

    logger.info("Starting bot")

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    register_all_middlewares(dp, config)
    # register_all_filters(dp)
    register_all_handlers(dp)

    await bot.set_my_commands([
        aiogram.types.BotCommand('weather', 'Узнать погоду'),
        aiogram.types.BotCommand('convert', 'Конвертировать валюту'),
        aiogram.types.BotCommand('cat', 'Случайная картинка с котиком'),
        aiogram.types.BotCommand('poll', 'Создать опрос'),
        aiogram.types.BotCommand('cancel', 'Отменить текущую команду'),
    ])

    session = await bot.get_session()

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
        logger.info("Bot stopped!")

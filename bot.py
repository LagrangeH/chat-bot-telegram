import asyncio

from aiogram.types import BotCommand
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import exceptions
from loguru import logger

from tgbot.config import load_config
from tgbot.handlers.user import register_user


def register_all_handlers(dp):
    register_user(dp)


async def main():
    config = load_config(".env")

    bot = Bot(token=config.api_keys.bot, parse_mode='HTML')
    dp = Dispatcher(bot, storage=MemoryStorage())

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

    logger.opt(colors=True).info(f"Bot started{' <blue>in debug mode</blue>' if config.debug else ''}")

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
    except exceptions.NetworkError:
        logger.error("Network error. Check internet connection")
    except Exception as e:
        logger.critical(f"Unexpected error: {e}")

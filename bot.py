import asyncio

from aiogram.types import BotCommand
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.utils import exceptions
from aiohttp import ClientSession
from environs import EnvError
from loguru import logger

from tgbot.config import load_config, Config
from tgbot.handlers.user import register_user
from tgbot.log_config import configure_loguru


async def set_bot_commands(bot: Bot) -> None:
    """
    Sets bot commands and saves them to bot config in readable format
    :param bot:
    :return:
    """
    await bot.set_my_commands([
        BotCommand('weather', 'Узнать погоду'),
        BotCommand('convert', 'Конвертировать валюту'),
        BotCommand('cat', 'Случайная картинка с котиком'),
        BotCommand('poll', 'Создать опрос'),
        BotCommand('cancel', 'Отменить текущую команду'),
        BotCommand('help', 'Вывести эту справку'),
    ])

    bot['config'].commands = '\n'.join([f"/{command[1]} - {descr[1]}"
                                        for command, descr in await bot.get_my_commands()])


async def run_bot(config: Config) -> None:
    logger.debug("Starting bot")
    bot = Bot(token=config.api_keys.bot, parse_mode='HTML')
    dp = Dispatcher(bot, storage=MemoryStorage())
    session: ClientSession = await bot.get_session()

    logger.debug("Configuring bot")
    bot['config'] = config
    register_user(dp)
    await set_bot_commands(bot)

    logger.opt(colors=True).info(f"Bot started{' <blue>in debug mode</blue>' if config.debug else ''}")

    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await session.close()


def main() -> None:
    try:
        configuration: Config = load_config(".env")
        configure_loguru(configuration.debug)
    except EnvError as e:
        logger.error(e)
    else:
        try:
            asyncio.run(run_bot(configuration))
        except (KeyboardInterrupt, SystemExit):
            logger.info("Bot stopped")
        except exceptions.NetworkError:
            logger.error("Network error. Check internet connection")
        except Exception as e:
            logger.opt(exception=configuration.debug).critical(f"Unexpected error: {e}")


if __name__ == '__main__':
    main()

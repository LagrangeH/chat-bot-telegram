import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher import DEFAULT_RATE_LIMIT
from aiogram.dispatcher.handler import current_handler, CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import Throttled
from loguru import logger


class ThrottlingMiddleware(BaseMiddleware):
    def __init__(self, limit=DEFAULT_RATE_LIMIT, key_prefix='antiflood_'):
        self.rate_limit = limit
        self.prefix = key_prefix
        super(ThrottlingMiddleware, self).__init__()

    async def on_process_message(self, message: Message, data: dict) -> None:
        await self._throttle(message, data)

    async def on_process_callback_query(self, callback_query: CallbackQuery, data: dict) -> None:
        await self._throttle(callback_query, data)

    async def _throttle(self, event: Message | CallbackQuery, data: dict) -> None:
        if not isinstance(event, (Message, CallbackQuery)):
            return

        # Get current handler
        handler = current_handler.get()
        # Get dispatcher from context
        dispatcher = Dispatcher.get_current()

        # If handler was configured, get rate limit and key from handler
        if handler:
            limit = getattr(handler, 'throttling_rate_limit', self.rate_limit)
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            limit = self.rate_limit
            key = f"{self.prefix}_{'message' if isinstance(event, Message) else 'callback_query'}"

        try:
            await dispatcher.throttle(key, rate=limit)

        except Throttled as t:
            await self.event_throttled(event, t)
            raise CancelHandler()

    async def event_throttled(self, event: Message | CallbackQuery, throttled: Throttled):
        """
        Notify user only on first exceed
        :param event:
        :param throttled:
        """
        handler = current_handler.get()

        if handler:
            key = getattr(handler, 'throttling_key', f"{self.prefix}_{handler.__name__}")
        else:
            key = f"{self.prefix}_{'message' if isinstance(event, Message) else 'callback_query'}"

        # Calculate how many times is left till the block ends
        delta = throttled.rate - throttled.delta

        # Prevent flooding
        if throttled.exceeded_count <= 2:
            logger.debug(f"Anti-flood: {key} exceeded {throttled.exceeded_count} times "
                         f"in {throttled.rate} seconds")
            await event.answer('Слишком много запросов!')

        # Stop processing animation on inline button for throttled queries
        elif isinstance(event, CallbackQuery):
            await event.bot.answer_callback_query(event.id)

        await asyncio.sleep(delta)


def rate_limit(limit: int, key: str = None):
    """
    Decorator for configuring rate limit and key in different functions
    :param limit:
    :param key:
    :return:
    """
    def decorator(func):
        setattr(func, 'throttling_rate_limit', limit)

        if key:
            setattr(func, 'throttling_key', key)
        return func

    return decorator

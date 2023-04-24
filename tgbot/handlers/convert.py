from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup
from loguru import logger

from tgbot.keyboards import inline
from tgbot.middlewares import throttling
from tgbot.misc.cute_cat import get_cat_picture
from tgbot.misc.exchange_rates import get_exchange_rate
from tgbot.misc.states import BotStates, ConvertStates
from tgbot.misc.weather import get_weather


async def convert_command(message: Message) -> None:
    """
    Handles /convert command.
    There are two ways to get the result:
        1. Via message
        2. Via inline keyboard

    :param message:
    :return:
    """
    logger.debug("Got /convert command")
    await message.reply(
        "Для конвертации изначальную валюту из списка или "
        "укажите данные для конвертации в таком формате:\n\n"
        "<code>100 USD RUB</code> - конвертирует 100 долларов в рубли",
        reply_markup=inline.currencies,
    )
    await ConvertStates.Convert.set()


@throttling.rate_limit(3, 'convert')
async def convert_message(message: Message, state: FSMContext) -> None:
    """
    Handles Convert state and sends converted currency
    :param message:
    :param state:
    :return:
    """
    logger.debug("Got currency for conversion in Convert state")
    await state.finish()

    amount, base, target = message.text.split(' ')
    if not amount.isdigit():
        await message.reply("Сумма должна быть числом. Попробуйте еще раз")
        return

    exchange_rate = get_exchange_rate(
        float(amount),
        base,
        target,
        message.bot['config'].api_keys.convert
    )

    if exchange_rate is None:
        await message.reply("Что-то пошло не так. Попробуйте еще раз")
    else:
        await message.reply(f"<code>{amount}</code> {base} = <code>{exchange_rate}</code> {target}")


async def convert_to_callback(query: CallbackQuery, state: FSMContext) -> None:
    """
    Handles if a user chooses to use the inline keyboard and selects the base currency
    :param query:
    :param state:
    :return:
    """
    # Parse query data provided by inline keyboard in format: 'convert_to:USD:0:0'
    query_data = query.data.split(':')

    await ConvertStates.ConvertTo.set()

    # Save base currency to state
    await state.update_data(base=query_data[1])

    # Remove chosen currency from inline keyboard
    edited_kb = inline.currencies
    edited_kb['inline_keyboard'][int(query_data[2])].pop(int(query_data[3]))

    # Send updated inline keyboard
    await query.bot.edit_message_text(
        "Теперь выберите валюту, в которую хотите конвертировать",
        query.from_user.id,
        query.message.message_id,
        reply_markup=edited_kb
    )


async def convert_from_callback(query: CallbackQuery, state: FSMContext) -> None:
    """
    Handles when user choose the target currency in second inline keyboard
    :param query:
    :param state:
    :return:
    """
    await ConvertStates.ConvertFrom.set()
    await state.update_data(target=query.data.split(':')[1])
    kb = inline.create_currency_amounts_kb()
    await query.bot.edit_message_text(
        "Введите или выберите сумму для конвертации",
        query.from_user.id,
        query.message.message_id,
        reply_markup=kb,
    )


async def convert_amount_callback(query: CallbackQuery, state: FSMContext) -> None:
    if 'base' not in await state.get_data() and 'target' not in await state.get_data():
        await query.bot.answer_callback_query(query.id, "Что-то пошло не так. Попробуйте еще раз")
        await ConvertStates.Convert.set()
        await query.answer(
            "Для конвертации изначальную валюту из списка или "
            "укажите данные для конвертации в таком формате:\n\n"
            "<code>100 USD RUB</code> - конвертирует 100 долларов в рубли",
            reply_markup=inline.currencies,
        )
        return

    amount = query.data.split(':')[1]
    data = await state.get_data()
    base, target = data['base'], data['target']
    exchange_rate = get_exchange_rate(
        float(amount),
        base,
        target,
        query.bot['config'].api_keys.convert,
    )
    if exchange_rate is None:
        await query.bot.send_message(query.from_user.id, "Что-то пошло не так. Попробуйте еще раз")
    else:
        await query.bot.edit_message_text(
            f"<code>{amount}</code> {base} = <code>{exchange_rate}</code> {target}",
            query.from_user.id,
            query.message.message_id,
            reply_markup=None,
        )
    await state.finish()


async def convert_operator_callback(query: CallbackQuery) -> None:
    """
    Handles when user clicks on the operator buttons to change the amount
    :param query:
    :return:
    """
    operator, amount = query.data.split(':')[1:]
    amount = int(amount)

    if operator == 'division':
        amount //= 10
    elif operator == 'multiplication':
        amount *= 10
    elif operator == 'subtraction':
        amount -= 10 ** len(str(amount)) // 10
    elif operator == 'addition':
        amount += 10 ** len(str(amount)) // 10

    await query.bot.edit_message_text(
        "Введите или выберите сумму для конвертации",
        query.from_user.id,
        query.message.message_id,
        reply_markup=inline.create_currency_amounts_kb(amount),
    )


async def convert_cansel_callback(query: CallbackQuery, state: FSMContext) -> None:
    logger.debug(f"Got cancel callback query in {await state.get_state()} state "
                 f"with data {await state.get_data()}")
    await query.bot.delete_message(query.from_user.id, query.message.message_id)
    await state.finish()


def register_convert(dp: Dispatcher) -> None:
    dp.register_message_handler(convert_command, commands=['convert'], state='*')
    dp.register_message_handler(convert_message, state=ConvertStates)
    dp.register_callback_query_handler(
        convert_to_callback,
        lambda c: c.data.startswith('currency'),
        state=ConvertStates.Convert,
    )
    dp.register_callback_query_handler(
        convert_from_callback,
        lambda c: c.data.startswith('currency'),
        state=ConvertStates.ConvertTo,
    )
    dp.register_callback_query_handler(
        convert_amount_callback,
        lambda c: c.data.startswith('amount'),
        state=ConvertStates.ConvertFrom,
    )
    dp.register_callback_query_handler(
        convert_operator_callback,
        lambda c: c.data.startswith('operator'),
        state='*'
    )
    dp.register_callback_query_handler(
        convert_cansel_callback,
        lambda c: c.data == 'cancel',
        state='*'
    )

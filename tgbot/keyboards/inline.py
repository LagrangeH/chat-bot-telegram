from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

cities = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Москва", callback_data="city:Москва"),
            InlineKeyboardButton(text="Санкт-Петербург", callback_data="city:Санкт-Петербург"),
        ],
        [
            InlineKeyboardButton(text="Екатеринбург", callback_data="city:Екатеринбург"),
            InlineKeyboardButton(text="Новосибирск", callback_data="city:Новосибирск"),
        ],
        [
            InlineKeyboardButton(text="Казань", callback_data="city:Казань"),
            InlineKeyboardButton(text="Красноярск", callback_data="city:Красноярск"),
        ],
        [
            InlineKeyboardButton(text="Минск", callback_data="city:Минск"),
            InlineKeyboardButton(text="Киев", callback_data="city:Киев"),
        ],
        [
            InlineKeyboardButton(text="Лондон", callback_data="city:Лондон"),
            InlineKeyboardButton(text="Париж", callback_data="city:Париж"),
        ],
    ],
)

currencies = InlineKeyboardMarkup(
    row_width=2,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Доллар США", callback_data="currency:USD:0:0"),
            InlineKeyboardButton(text="Евро", callback_data="currency:EUR:0:1"),
        ],
        [
            InlineKeyboardButton(text="Российский рубль", callback_data="currency:RUB:1:0"),
            InlineKeyboardButton(text="Украинская гривна", callback_data="currency:UAH:1:1"),
        ],
        [
            InlineKeyboardButton(text="Белорусский рубль", callback_data="currency:BYN:2:0"),
            InlineKeyboardButton(text="Казахстанский тенге", callback_data="currency:KZT:2:1"),
        ],
        [
            InlineKeyboardButton(text="Японская иена", callback_data="currency:JPY:3:0"),
            InlineKeyboardButton(text="Фунт стерлингов", callback_data="currency:GBP:3:1"),
        ],
        [
            InlineKeyboardButton(text="Швейцарский франк", callback_data="currency:CHF:4:0"),
            InlineKeyboardButton(text="Канадский доллар", callback_data="currency:CAD:4:1"),
        ],
        [
            InlineKeyboardButton(text="Австралийский доллар", callback_data="currency:AUD:5:0"),
            InlineKeyboardButton(text="Новозеландский доллар", callback_data="currency:NZD:5:1"),
        ],
        [
            InlineKeyboardButton(text="Китайский юань", callback_data="currency:CNY:6:0"),
            InlineKeyboardButton(text="Шведская крона", callback_data="currency:SEK:6:1"),
        ],
        [
            InlineKeyboardButton(text="Турецкая лира", callback_data="currency:TRY:7:0"),
            InlineKeyboardButton(text="Израильский шекель", callback_data="currency:ILS:7:1"),
        ],
        [
            InlineKeyboardButton(text="Индийская рупия", callback_data="currency:INR:8:0"),
            InlineKeyboardButton(text="Южноафриканский рэнд", callback_data="currency:ZAR:8:1"),
        ],

        [
            InlineKeyboardButton(text="Отмена", callback_data="cancel"),
        ],
    ]
)


def create_currency_amounts_kb(amount: float | int = 100) -> InlineKeyboardMarkup:
    term = 10 ** len(str(amount)) // 10
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f"{amount}", callback_data=f"amount:{amount}"),
            ],
            [
                InlineKeyboardButton(text="÷10", callback_data=f"operator:division:{amount}"),
                InlineKeyboardButton(text=f"-{term}", callback_data=f"operator:subtraction:{amount}"),
                InlineKeyboardButton(text=f"+{term}", callback_data=f"operator:addition:{amount}"),
                InlineKeyboardButton(text="×10", callback_data=f"operator:multiplication:{amount}"),
            ],
            [
                InlineKeyboardButton(text="Отмена", callback_data="cancel"),
            ]
        ]
    )

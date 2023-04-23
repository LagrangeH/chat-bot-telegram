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

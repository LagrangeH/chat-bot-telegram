import requests

from tgbot.misc.cute_cat import get_cat_picture
from tgbot.misc.exchange_rates import get_exchange_rate


def test_cat_without_api_key():
    result = get_cat_picture("wrong_api_key")
    response = requests.get(result)
    response.raise_for_status()


def test_exchange_rate_with_wrong_api_key():
    result = get_exchange_rate(500, "USD", "RUB", "wrong_api_key")
    assert result is None

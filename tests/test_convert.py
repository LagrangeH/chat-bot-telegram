import pytest

from tgbot.misc.exchange_rates import get_exchange_rate


def test_exchange_rate_without_api_key():
    result = get_exchange_rate(500, "USD", "RUB", "wrong_api_key")
    assert result is None


def test_exchange_rate_with_api_key(request):
    api_key = request.config.getoption("--exchange-api-key")
    if api_key is None:
        pytest.skip(reason="No exchange api key provided")

    result = get_exchange_rate(500, "USD", "RUB", api_key)
    assert isinstance(result, float)


def test_exchange_rate_with_wrong_currency(request):
    api_key = request.config.getoption("--exchange-api-key")
    if api_key is None:
        pytest.skip(reason="No exchange api key provided")

    result = get_exchange_rate(500, "USD", "WRONG", api_key)
    assert result is None

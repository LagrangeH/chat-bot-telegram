import pytest

from tgbot.misc.weather import get_weather


def test_weather_with_wrong_api_key():
    result = get_weather("Moscow", "wrong_api_key")
    assert result is None


def test_weather_with_api_key(request):
    api_key = request.config.getoption("--weather-api-key")
    if api_key is None:
        pytest.skip(reason="No weather api key provided")

    result = get_weather("Moscow", api_key)
    assert isinstance(result, dict)
    assert result["description"] is not None
    assert isinstance(result["description"], str)
    assert -274 < result["temperature"] < 200
    assert -274 < result["feels_like"] < 200
    assert 0 <= result["humidity"] <= 100
    assert 0 <= result["wind_speed"] <= 100


def test_weather_with_wrong_city(request):
    api_key = request.config.getoption("--weather-api-key")
    if api_key is None:
        pytest.skip(reason="No weather api key provided")

    result = get_weather("_Moscow_", api_key)
    assert result is None

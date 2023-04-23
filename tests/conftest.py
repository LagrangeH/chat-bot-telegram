from environs import Env


def pytest_addoption(parser):
    """
    Add options to pytest from the command line if available,
    or from the .env file otherwise None values will be passed

    Usage:
    ******

        >>> import pytest
        >>> def test_cat(request):
        >>>    api_key = request.config.getoption("--cat-api-key")
        >>>    if api_key is None:
        >>>        pytest.skip(reason="No cat api key provided")
        >>>    ...

    :param parser:
    :return:
    """
    env = Env()
    env.read_env('.env')

    parser.addoption(
        "--cat-api-key",
        action="store",
        default=env.str("CAT_API_KEY", None),
        help="Cat API key",
    )
    parser.addoption(
        "--exchange-api-key",
        action="store",
        default=env.str("EXCHANGE_API_KEY", None),
        help="Exchange Rates API key",
    )
    parser.addoption(
        "--weather-api-key",
        action="store",
        default=env.str("WEATHER_API_KEY", None),
        help="Open Weather Map API key",
    )

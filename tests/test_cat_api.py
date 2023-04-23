import pytest
import requests

from tgbot.misc.cute_cat import get_cat_picture


def test_cat_without_api_key():
    cat_link = get_cat_picture("wrong_api_key")
    response = requests.get(cat_link)
    response.raise_for_status()


def test_cat_with_api_key(request):
    api_key = request.config.getoption("--cat-api-key")
    if api_key is None:
        pytest.skip(reason="No cat api key provided")
    cat_link = get_cat_picture(api_key)
    response = requests.get(cat_link)
    response.raise_for_status()

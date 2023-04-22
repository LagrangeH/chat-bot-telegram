from pprint import pprint

import requests
from loguru import logger


def kelvin_to_celsius(temperature: float | int) -> float:
    """
    Convert temperature from Kelvin to Celsius rounded to 1 decimal place
    :param temperature:
    :return:
    """
    return round(temperature - 273.15, 1)


def get_weather(city: str, api_key) -> dict[str, str | float | int] | None:
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=ru'

    response = requests.get(url)
    if response.status_code != 200:
        return None

    data = response.json()
    logger.debug(f"Got weather in {city}")
    return {
        'description': data['weather'][0]['description'],
        'temperature': kelvin_to_celsius(data['main']['temp']),
        'feels_like': kelvin_to_celsius(data['main']['feels_like']),
        'humidity': data['main']['humidity'],
        'wind_speed': data['wind']['speed'],
    }


if __name__ == '__main__':
    pprint(get_weather('Moscow', input('Enter API key: ')))

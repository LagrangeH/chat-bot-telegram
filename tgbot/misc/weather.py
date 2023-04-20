from pprint import pprint

import requests


def kelvin_to_celsius(temperature: float) -> float:
    return round(temperature - 273.15, 1)


def get_weather(city: str, api_key):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=ru'

    response = requests.get(url)
    if response.status_code != 200:
        return None

    data = response.json()
    return {
        'description': data['weather'][0]['description'],
        'temperature': kelvin_to_celsius(data['main']['temp']),
        'feels_like': kelvin_to_celsius(data['main']['feels_like']),
        'humidity': data['main']['humidity'],
        'wind_speed': data['wind']['speed'],
    }


if __name__ == '__main__':
    pprint((get_weather('Moscow', input('Enter API key: '))))

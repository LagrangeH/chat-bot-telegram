import requests


def get_exchange_rate(amount: int | float, base: str, target: str, api_key) -> float | None:
    response = requests.get(
        f"https://api.apilayer.com/exchangerates_data/convert?to={target}&from={base}&amount={amount}",
        headers={'apikey': api_key}
    )

    if response.status_code != 200:
        return None

    return round(response.json()['result'], 2)


if __name__ == '__main__':
    print(get_exchange_rate(500, "USD", "RUB", input('Enter API key: ')))

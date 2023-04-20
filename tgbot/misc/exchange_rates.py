import requests


async def get_exchange_rate(base: str, target: str):
    # TODO
    response = requests.get(f"https://api.exchangeratesapi.io/latest?base={base}&symbols={target}")
    if response.status_code != 200:
        return None
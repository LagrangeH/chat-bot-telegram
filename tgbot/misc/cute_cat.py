import requests


def get_cat_picture(api_key) -> str | None:
    """
    Get random picture from thecatapi.com
    :param api_key:
    :return: Link to picture or None if error
    """
    response = requests.get(f'https://api.thecatapi.com/v1/images/search'
                            f'{"" if api_key is None else f"?api_key={api_key}"}')
    if response.status_code != 200:
        return None

    # data = json.loads(response.text)[0]
    return response.json()[0]['url']

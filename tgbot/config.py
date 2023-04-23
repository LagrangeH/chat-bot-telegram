import sys
from dataclasses import dataclass

from environs import Env
from loguru import logger


@dataclass
class APIKeys:
    bot: str
    cat: str
    weather: str
    convert: str


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    api_keys: APIKeys
    misc: Miscellaneous
    debug: bool


def load_config(path: str = None) -> Config:
    env = Env()
    env.read_env(path)

    return Config(
        api_keys=APIKeys(
            bot=env.str("BOT_TOKEN"),
            cat=env.str("CAT_API_KEY", None),
            weather=env.str("WEATHER_API_KEY"),
            convert=env.str("EXCHANGE_API_KEY"),
        ),
        debug=env.bool('DEBUG', False),
        misc=Miscellaneous(),
    )

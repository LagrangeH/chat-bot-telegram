from dataclasses import dataclass

from environs import Env
from loguru import logger


@dataclass
class DbConfig:
    host: str
    password: str
    user: str
    database: str


@dataclass
class TgBot:
    token: str
    admin_ids: list[int]
    use_redis: bool


@dataclass
class Miscellaneous:
    other_params: str = None


@dataclass
class Config:
    tg_bot: TgBot
    db: DbConfig
    misc: Miscellaneous
    debug: bool
    cat_api_key: str
    weather_api_key: str
    exchange_api_key: str


def load_config(path: str = None):
    logger.debug("Loading config")
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBot(
            token=env.str("BOT_TOKEN"),
            admin_ids=list(map(int, env.list("ADMINS"))),
            use_redis=env.bool("USE_REDIS"),
        ),
        db=DbConfig(
            host=env.str('DB_HOST'),
            password=env.str('DB_PASS'),
            user=env.str('DB_USER'),
            database=env.str('DB_NAME')
        ),
        misc=Miscellaneous(),
        debug=env.bool('DEBUG', False),
        cat_api_key=env.str("CAT_API_KEY", None),
        weather_api_key=env.str("WEATHER_API_KEY"),
        exchange_api_key=env.str("EXCHANGE_API_KEY"),
    )

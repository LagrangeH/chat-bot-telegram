import sys

from loguru import logger


def configure_loguru(debug: bool = False) -> None:
    """
    Delete existing handlers and add the specified ones
    :param debug: If True, then the debug level will be set
    :return:
    """
    logger.remove()

    logger.add(
        sys.stdout,
        level="DEBUG" if debug else "INFO",
        colorize=True,
        serialize=False,
        backtrace=debug,
        diagnose=debug,
        enqueue=not debug,
        catch=True,
    )

    logger.add(
        "logs/error.log",
        level="ERROR",
        format="{time} | {file}:{function}:{line} - {message}",
        colorize=False,
        serialize=False,
        backtrace=False,
        diagnose=False,
        enqueue=True,
        catch=True,
        rotation="10 MB",
        retention="1 month",
        compression="zip",
        delay=True,
    )

    if debug:
        logger.add(
            "logs/debug.log",
            level="DEBUG",
            colorize=False,
            serialize=False,
            backtrace=True,
            diagnose=True,
            enqueue=False,
            catch=True,
            rotation="10 MB",
            retention="1 month",
            compression="zip",
            delay=True,
        )

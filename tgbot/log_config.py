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
        enqueue=False,
        catch=True,
    )


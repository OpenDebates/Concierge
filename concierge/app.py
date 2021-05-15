import logging
import sys

import toml

import concierge
from concierge.bot import bot
from concierge.server import app

logger = logging.getLogger(__name__)
root_logger = logger.parent


def start_server(**kwargs):
    """
    Starts the server and obtains all necessary config data.
    """
    if kwargs["log_level"]:
        # Set logger level
        level = logging.getLevelName(kwargs["log_level"].upper())
        root_logger.setLevel(level)
    else:
        root_logger.setLevel("INFO")

    # Config Loader
    config = toml.load("config.toml")
    logger.info(f"Starting Concierge Server: {concierge.__version__}")

    try:
        app.run(host=config['server']['host'], port=config['server']['port'])
    finally:
        sys.exit()


def start_bot(**kwargs):
    """
    Starts the bot and obtains all necessary config data.
    """
    if kwargs["log_level"]:
        # Set logger level
        level = logging.getLevelName(kwargs["log_level"].upper())
        root_logger.setLevel(level)
    else:
        root_logger.setLevel("INFO")

    # Config Loader
    config = toml.load("config.toml")
    logger.info(f"Starting Concierge Bot: {concierge.__version__}")

    bot.ipc.start()
    bot.run(config["bot"]["token"])

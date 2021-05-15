import logging

import discord
import toml
from discord.ext import commands, ipc

logger = logging.getLogger(__name__)
config = toml.load("config.toml")


class ConciergeBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.ipc = ipc.Server(self, secret_key=config["global"]["ipc_secret"])  # create our IPC Server

    async def on_ready(self):
        """Called upon the READY event"""
        logger.info("Bot is ready.")

    async def on_ipc_ready(self):
        """Called upon the IPC Server being ready"""
        logger.info("IPC is ready.")

    async def on_ipc_error(self, endpoint, error):
        """Called upon an error being raised within an IPC route"""
        logger.info(endpoint, "raised", error)


bot = ConciergeBot(command_prefix="+", intents=discord.Intents.all())


@ipc.server.route()
async def on_webhook_received(data):
    logger.info(data.request_json)
    return True

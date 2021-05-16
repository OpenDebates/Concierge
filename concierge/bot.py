import asyncio
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

    async def on_member_join(self, member):
        await asyncio.sleep(3)
        guild = bot.get_guild(config["bot"]["guild_id"])
        general_tc = discord.utils.get(guild.channels, name="general")
        about_tc = discord.utils.get(guild.channels, name="about")
        rules_tc = discord.utils.get(guild.channels, name="rules")
        embed = discord.Embed(
            description=f"Welcome to Open Debates!\n"
                        f"\n"
                        f"This server is unique in that debates can take place "
                        f"through an ELO rating system. To learn more, please "
                        f"watch this [video](https://www.youtube.com/watch?v=L2NthdKPLZQ)."
                        f"You can also pick up some roles and learn more about the server "
                        f"from the {about_tc.mention} section.  In addition, "
                        f"please ensure you've read and understood "
                        f"the {rules_tc.mention} to make your stay worthwhile."
        )
        embed.set_footer(text=member.name, icon_url=member.avatar_url)
        member_role = discord.utils.get(guild.roles, name="Member")
        if member_role in member.roles:
            await general_tc.send(embed=embed)


bot = ConciergeBot(command_prefix="+", intents=discord.Intents.all())
bot.remove_command("help")


@bot.ipc.route()
async def on_webhook_received(data):
    request = data.request_json
    if request['OP'] == 1:
        guild = bot.get_guild(config["bot"]["guild_id"])
        general_tc = discord.utils.get(guild.channels, name="general")
        about_tc = discord.utils.get(guild.channels, name="about")
        rules_tc = discord.utils.get(guild.channels, name="rules")
        member = guild.get_member(int(request['member']['id']))
        embed = discord.Embed(
            description=f"Welcome to Open Debates!\n"
                        f"\n"
                        f"This server is unique in that debates can take place "
                        f"through an ELO rating system. To learn more, please "
                        f"watch this [video](https://www.youtube.com/watch?v=L2NthdKPLZQ)."
                        f"You can also pick up some roles and learn more about the server "
                        f"from the {about_tc.mention} section.  In addition, "
                        f"please ensure you've read and understood "
                        f"the {rules_tc.mention} to make your stay worthwhile."
        )
        embed.set_footer(text=member.name, icon_url=member.avatar_url)
        await general_tc.send(embed=embed)
    elif request['OP'] == 5:
        logger.info(f"Test Webhook: {request}")
    return True


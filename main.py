from pathlib import Path

from discord import Activity
from discord import ActivityType
from discord import Intents
from discord import Status
from discord.ext.commands import Bot

from data import read
from data.constants import GUILD


class CommandsBot(Bot):

    def __init__(self):

        super().__init__(
            activity=Activity(
                name="8574",
                type=ActivityType.watching),
            command_prefix="aanniimmee",
            help_command=None,
            intents=Intents(
                guilds=True,
                guild_messages=True,
                message_content=True),
            status=Status.online)

    async def setup_hook(self) -> None:

        for command in Path("ext").glob("*.py"):
            command = str(command).replace("\\", ".").replace("/", ".")[:-3]
            if command not in ("ext._template", "ext.error_handler"):
                # Load ext
                await self.load_extension(command)
                print(f"Loaded {command}")

        print()
        self.tree.copy_global_to(guild=GUILD)
        await self.tree.sync(guild=GUILD)


bot = CommandsBot()
bot.run(read("config", "token"))

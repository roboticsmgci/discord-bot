from discord import Interaction
from discord.app_commands import command
from discord.app_commands import guilds
from discord.ext.commands import Cog

from data.constants import GUILD


async def setup(bot):
    await bot.add_cog(Test(bot), guild=GUILD)


@guilds(GUILD)
class Test(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command(name="test")
    async def select(self, interaction: Interaction):

        raise Exception("test")

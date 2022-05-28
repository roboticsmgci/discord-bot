from discord import Interaction
from discord.app_commands import command
from discord.app_commands import guilds
from discord.ext.commands import Cog

from data.constants import GUILD, ELEVATED_USERS


async def setup(bot):
    await bot.add_cog(Admin(bot), guild=GUILD)


@guilds(GUILD)
class Admin(Cog):

    def __init__(self, bot):
        self.bot = bot

    @command(name="end")
    async def end(self, interaction: Interaction):

        if interaction.user.id not in ELEVATED_USERS:
            await interaction.response.send_message(
                f"{interaction.user.mention}, you do not have permission to use this command.",
                ephemeral=True)
            return

        await interaction.response.send_message(
            f"{interaction.user.mention}, closing bot.",
            ephemeral=True)
        await self.bot.close()

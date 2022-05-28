from random import choice
from random import randint
from re import sub, search

from aiohttp import ClientSession
from discord import Colour
from discord import Interaction
from discord import Member
from discord import Message
from discord.app_commands import command
from discord.app_commands import describe
from discord.app_commands import guilds
from discord.ext.commands import Cog
from discord.ext.commands import GroupCog

from data import read
from data import write_value
from data.constants import ELEVATED_USERS
from data.constants import GUILD


def random_ending():
    return choice(
        ["uwu", "owo", "(ᵘʷᵘ)", "(◡ ω ◡)", "(˘ω˘)", "(˘ε˘)", "( ´ω` )", "(*ฅ́˘ฅ̀*)", "ღ(U꒳Uღ)",
         "(*´▽`*)", "(o^▽^o)", "＼(￣▽￣)／", "＼(＾▽＾)／", "(ﾉ◕ヮ◕)ﾉ*:･ﾟ✧", "( ◕▿◕ )", "(♡°▽°♡)",
         "♡＼(￣▽￣)／♡", "(⁄ ⁄•⁄ω⁄•⁄ ⁄)", "(⁄ ⁄>⁄ ▽ ⁄<⁄ ⁄)", "╮(￣～￣)╭", "(◎ ◎)ゞ", "(￢_￢)",
         "(⊙_⊙)", "(・∀・)ノ", "	＼(⌒▽⌒)", "	(o´▽`o)ﾉ", "ヾ(・ω・*)", "(≧▽≦)/", "(*・ω・)ﾉ",
         "(づ￣ ³￣)づ", "(っಠ‿ಠ)っ", "(つ✧ω✧)つ", "⊂( ´ ▽ ` )⊃", "(^_<)〜☆", "(￣ ;;￣)",
         "┬┴┬┴┤(･_├┬┴┬┴", "(^=◕ᴥ◕=^)", "ଲ(ⓛ ω ⓛ)ଲ", "	ʕ •̀ ω •́ ʔ", "／(＞×＜)＼", "(っ˘ڡ˘ς)"]
        + ["nya"] * 3 + ["nye"] * 3 + ["peko"] * 2 + [""] * 10)


async def setup(bot):
    await bot.add_cog(Imposter(bot), guild=GUILD)


@guilds(GUILD)
class Imposter(GroupCog, group_name="imposter"):

    def __init__(self, bot):
        self.bot = bot
        self.target = read("misc", "imposter_target")

        if type(self.target) == str:
            self.target = int(self.target)

    @command(name="select", description="Choose a person for this bot to become.")
    @describe(member="The victim")
    async def select(self, interaction: Interaction, member: Member):

        if interaction.user.id not in ELEVATED_USERS:
            await interaction.response.send_message(
                f"{interaction.user.mention}, you do not have permission to use this command.",
                ephemeral=True)
            return

        self.target = member.id
        write_value("misc", imposter_target=str(member.id))
        await interaction.response.send_message(
            f"{interaction.user.mention}, preparing to become {member.mention}. This process might take a few minutes.",
            ephemeral=True)

        async with ClientSession() as cs:
            async with cs.get(member.avatar.url) as pfp:
                await self.bot.user.edit(avatar=await pfp.read())

        me = await interaction.guild.fetch_member(961327910499795034)
        await me.edit(nick=member.nick)
        await interaction.guild.get_role(979758631404863568).edit(colour=member.colour)

        await interaction.edit_original_message(
            content=f"{interaction.user.mention}, sucessfully become {member.mention}."
        )

    @command(name="remove", description="Become normal again")
    async def remove(self, interaction: Interaction):

        if interaction.user.id not in ELEVATED_USERS:
            await interaction.response.send_message(
                f"{interaction.user.mention}, you do not have permission to use this command.",
                ephemeral=True)
            return

        self.target = None
        write_value("misc", imposter_target=None)
        await interaction.response.send_message(
            f"{interaction.user.mention}, preparing to become normal. This process might take a few minutes.",
            ephemeral=True)

        await self.bot.user.edit(avatar=None)

        me = await interaction.guild.fetch_member(961327910499795034)
        await me.edit(nick="8574_02")
        await interaction.guild.get_role(979758631404863568).edit(colour=Colour.light_grey())

        await interaction.edit_original_message(
            content=f"{interaction.user.mention}, sucessfully become normal."
        )

    @Cog.listener()
    async def on_message(self, message: Message):

        if message.author.id != self.target:
            return

        text = message.content

        # Really > Weawwy
        text = text.replace("r", "w").replace("l", "w").replace("R", "W").replace("L", "W")

        # Thing > Fing, Love > Luv
        # I'm not gonna bother with all case variants, only bothering with lower, upper, and title
        text = text.replace("that", "dat").replace("THAT", "DAT").replace("That", "Dat")
        text = text.replace("th", "f").replace("TH", "F").replace("Th", "F")
        text = text.replace("ove", "uv").replace("OVE", "UV").replace("Ove", "Uv")

        # Nya Nye Nyi Nyo Nyu
        text = sub(r"n([aeiou])", r"ny\1", text)
        text = sub(r"n([AEIOU])", r"ny\1", text)
        text = sub(r"N([aeiou])", r"Ny\1", text)
        text = sub(r"N([AEIOU])", r"Ny\1", text)

        # Stutter
        words = text.split(" ")
        for i in range(len(words)):
            for prefix in ("i", "I", "d", "D", "n", "N", "w", "W"):
                if words[i].startswith(prefix):
                    if randint(0, 7) == 0:
                        words[i] = f"{prefix}-{prefix}{words[i][1:]}"
        text = " ".join(words)

        # Ending ehe
        text = "\n".join(f"{line} {random_ending()}" if line != "" else "" for line in text.split("\n"))

        # Remove mass mention
        text = text.replace("@everyone", "@everyonе").replace("@here", "@herе")
        # Remove role mention
        pattern = r"<@&([0-9]{18})>"
        res = search(pattern, text)
        while res is not None:
            try:
                mentioned_role = message.guild.get_role(int(res.group()[3:-1]))
                if mentioned_role is None:
                    raise ValueError
            except ValueError:
                text = text.replace(res.group(), "@deleted-role")
            else:
                text = text.replace(res.group(), f"@{mentioned_role.name}")
            res = search(pattern, text)

        await message.delete()
        await message.channel.send(text)

from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
import discord
import random as r
import io
from io import BytesIO
import aiohttp

import functions
from discord_components import DiscordComponents, Button, ButtonStyle, Select, SelectOption


class MainCog(commands.Cog, name='messages'):
    """Commands will make ur server better"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setphishing(self, ctx, val: int):
        '''1 arg: 0 or 1'''
        functions.updatesql(server=ctx.guild.id, links=val)
        if 0 <= val <= 1:
            await ctx.send(embed=discord.Embed(title='Done :)', color=0x00ff00))
        else:
            await ctx.send(embed=discord.Embed(title='Value must be 0 or 1', color=0xff0000))


def setup(bot):
    bot.add_cog(MainCog(bot))

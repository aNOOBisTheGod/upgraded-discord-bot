from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
import discord
import random as r
import io
from io import BytesIO
import aiohttp
import functions as func
from discord_components import DiscordComponents, Button, ButtonStyle, Select, SelectOption


class MainCog(commands.Cog, name='filters'):
    '''Commands in here can make your image beautiful'''

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def filter(self, ctx):
        '''all filters in this command'''
        attachment = ctx.message.attachments[0]
        await ctx.send(
            embed=discord.Embed(description=f'What do you like to do with that image?'),
            components=[
                Select(
                    placeholder="Choose action!",
                    options=[
                        SelectOption(label="make anagliph", value="a"),
                        SelectOption(label="reverse colors", value="b"),
                    ]
                )
            ]
        )
        colors = [0xFFE4E1, 0x00FF7F, 0xD8BFD8, 0xDC143C, 0xFF4500, 0xDEB887, 0xADFF2F, 0x800000, 0x4682B4, 0x006400,
                  0x808080, 0xA0522D, 0xF08080, 0xC71585, 0xFFB6C1, 0x00CED1]
        interaction = await self.bot.wait_for("select_option")
        if interaction.component[0].value == 'a':
            await interaction.respond(content=f'(☞ﾟヮﾟ)☞')
            with io.BytesIO() as image_binary:
                func.anagliph(attachment.url).save(image_binary, 'PNG')
                image_binary.seek(0)
                await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))
        elif interaction.component[0].value == 'b':
            await interaction.respond(content=f'╰(*°▽°*)╯')
            with io.BytesIO() as image_binary:
                func.reverse(attachment.url).save(image_binary, 'PNG')
                image_binary.seek(0)
                await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))


def setup(bot):
    bot.add_cog(MainCog(bot))
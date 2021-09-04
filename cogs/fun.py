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


class MainCog(commands.Cog, name='fun'):
    """Commands in this module was made to make you happy))"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def action(self, ctx, member: discord.Member):
        """choose what to do with somebody"""
        await ctx.send(
            embed=discord.Embed(description=f'Ok, so what do you want to do with {member}?'),
            components=[
                Select(
                    placeholder="Choose action!",
                    options=[
                        SelectOption(label="hug", value="a"),
                        SelectOption(label="poke", value="b"),
                        SelectOption(label="kiss", value="c"),
                        SelectOption(label="punch", value="d"),
                        SelectOption(label="kill", value="e"),
                        SelectOption(label="say hello", value="f"),
                        SelectOption(label="say goodbye", value="g"),
                    ]
                )
            ]
        )
        colors = [0xFFE4E1, 0x00FF7F, 0xD8BFD8, 0xDC143C, 0xFF4500, 0xDEB887, 0xADFF2F, 0x800000, 0x4682B4, 0x006400,
                  0x808080, 0xA0522D, 0xF08080, 0xC71585, 0xFFB6C1, 0x00CED1]
        interaction = await self.bot.wait_for("select_option")
        if interaction.component[0].value == 'a':
            await interaction.respond(content=f'so cute(*/ω＼*)')
            embed = discord.Embed(
                title=f'{ctx.message.author} hugged {member}',
                color=r.choice(colors)
            )
            embed.set_image(url=r.choice(['https://imgur.com/KzIOxZu',
                                          'https://rusinfo.info/wp-content/uploads/e/5/c'
                                          '/e5ccdbd4265374557a50e408191f2eeb.gif']))
            await ctx.send(embed=embed)
        elif interaction.component[0].value == 'b':
            await interaction.respond(content=f'(☞ﾟヮﾟ)☞')
            embed = discord.Embed(
                title=f'{ctx.message.author} poked {member}',
                color=r.choice(colors)
            )
            embed.set_image(url='https://thumbs.gfycat.com/EnlightenedInferiorAfricanaugurbuzzard-size_restricted.gif')
            await ctx.send(embed=embed)
        elif interaction.component[0].value == 'c':
            await interaction.respond(content=f'(¬‿¬)')
            await interaction.respond(content=f'so cute(*/ω＼*)')
            embed = discord.Embed(
                title=f'{ctx.message.author} kissed {member}',
                color=r.choice(colors)
            )
            embed.set_image(url='https://data.whicdn.com/images/209268053/original.gif')
            await ctx.send(embed=embed)
        elif interaction.component[0].value == 'd':
            await interaction.respond(content=f'ok, sir')
            embed = discord.Embed(
                title=f'{ctx.message.author} punched {member}',
                color=r.choice(colors)
            )
            embed.set_image(url=r.choice(['https://images2.minutemediacdn.com/image/fetch/c_fill,g_auto,f_auto,h_560,'
                                            'w_850/https%3A%2F%2Fmedia.giphy.com%2Fmedia%2FiWEIxgPiAq58c%2Fgiphy.gif',
                                          'https://media.discordapp.net/attachments/610489256518877184'
                                          '/611118922422288384/80kI.gif']))
            await ctx.send(embed=embed)
        elif interaction.component[0].value == 'e':
            await interaction.respond(content=f'y r u so cruel?')
            embed = discord.Embed(
                title=f'{ctx.message.author} killed {member}',
                color=r.choice(colors)
            )
            embed.set_image(url='http://www.the-arcade.ie/wp-content/uploads/2016/09'
                                '/tumblr_nkisa9gQYp1r3nw1vo2_500_700x330.gif')
            await ctx.send(embed=embed)
        elif interaction.component[0].value == 'f':
            await interaction.respond(content=f'done')
            embed = discord.Embed(
                title=f'{ctx.message.author} said hello to {member}',
                color=r.choice(colors)
            )
            embed.set_image(url='https://mondrian.mashable.com/wp-content%252Fuploads%252F2013%252F06%252FWaving'
                                '-Ariel-GIF.gif%252Ffull-fit-in__1200x2000.gif?signature=nMnY2uSIsnjgMkL69tqTvH4hAXs'
                                '=&source=http%3A%2F%2Fmashable.com')
            await ctx.send(embed=embed)
        elif interaction.component[0].value == 'g':
            await interaction.respond(content=f'done')
            embed = discord.Embed(
                title=f'{ctx.message.author} said goodbye to {member}',
                color=r.choice(colors)
            )
            embed.set_image(url='https://thumbs.gfycat.com/ConstantWealthyIcefish-size_restricted.gif')
            await ctx.send(embed=embed)

    # @commands.command()
    # async def messages(self, ctx):
    #     counter = 0
    #     for member in ctx.guild.members:
    #         for channel in ctx.guild.channels:
    #             print(channel)
    #             try:
    #                 async for message in channel.history():
    #                     if message.author == member:
    #                         counter += 1
    #             except:
    #                 continue
    #         await ctx.send(f'{member.mention} has sent **{counter}** messages in this server.')




def setup(bot):
    bot.add_cog(MainCog(bot))
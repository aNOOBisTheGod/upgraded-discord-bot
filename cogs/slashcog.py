from discord.ext import commands
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_choice, create_option
import discord
import random as r
import io
from io import BytesIO
import aiohttp

import functions
import functions as func
from discord_components import DiscordComponents, Button, ButtonStyle, Select, SelectOption
from bot import guild_ids_list
import datetime


class MainCog(commands.Cog, name='slash'):
    '''all commands in here are slash commands, you can view them
    by typing /'''

    def __init__(self, bot):
        self.bot = bot

    @cog_ext.cog_slash(name="server",
                       guild_ids=guild_ids_list,
                       description='sends info about server random number')
    async def server(self, ctx: SlashContext):
        print(guild_ids_list)
        server = ctx.guild
        online = 0
        for i in server.members:
            if str(i.status) == 'online' or str(i.status) == 'idle' or str(i.status) == 'dnd':
                online += 1
        channel_count = len([i for i in server.channels if type(i) == discord.channel.TextChannel])
        role_count = len(server.roles)
        emoji_count = len(server.emojis)
        em = discord.Embed(color=discord.Colour.from_rgb(232, 111, 108))
        em.add_field(name='Name', value=server.name)
        em.add_field(name='Owner', value=server.owner)
        em.add_field(name='Members', value=server.member_count)
        em.add_field(name='Currently Online', value=online)
        em.add_field(name='Text Channels', value=str(channel_count))
        em.add_field(name='Region', value=server.region)
        em.add_field(name='Verification Level', value=str(server.verification_level))
        em.add_field(name='Number of roles', value=str(role_count))
        em.add_field(name='Number of emotes', value=str(emoji_count))
        em.add_field(name='Created At', value=server.created_at.__format__('%A, %d. %B %Y @ %H:%M:%S'))
        em.set_thumbnail(url=server.icon_url)
        em.set_author(name='Server Info', icon_url='https://cdn.discordapp.com/emojis/762419676755787806.png?v=1')
        em.set_footer(text='Server ID: %s' % server.id)
        await ctx.send(embed=em)

    @cog_ext.cog_slash(name="random",
                       guild_ids=guild_ids_list,
                       description='generates random number',
                       options=[
                           create_option(
                               name='to',
                               description='sets 1st number',
                               option_type=4,
                               required=True
                           ),
                           create_option(
                               name='f',
                               description='sets 1st number',
                               option_type=4,
                               required=False
                           ),
                       ])
    async def random(self, ctx: SlashContext, to: int, f=0):
        await ctx.send(str(r.randint(f, to)))

    # @cog_ext.cog_slash(name="createemoji",
    #                    guild_ids=guild_ids_list,
    #                    description='creates emoji by url',
    #                    options=[
    #                        create_option(
    #                            name='url',
    #                            description='url of emoji picture',
    #                            option_type=3,
    #                            required=True
    #                        ),
    #                        create_option(
    #                            name='name',
    #                            description='name of emoji',
    #                            option_type=3,
    #                            required=True
    #                        ),
    #                    ])
    # async def createemoji(self, ctx: SlashContext, url: str, name: str):
    #     """creates custom emoji(staff only)"""
    #     if ctx.author.guild_permissions.manage_messages:
    #         async with aiohttp.ClientSession() as ses:
    #             async with ses.get(url) as r:
    #                 try:
    #                     img_or_gif = BytesIO(await r.read())
    #                     b_value = img_or_gif.getvalue()
    #                     if r.status in range(200, 299):
    #                         emoji = await ctx.guild.create_custom_emoji(image=b_value, name=name)
    #                         await ctx.send(f'Successfully created emoji: <:{name}:{emoji.id}>')
    #                         await ses.close()
    #                     else:
    #                         await ctx.send(f'Error when making request | {r.status} response.')
    #                         await ses.close()
    #                 except discord.HTTPException:
    #                     await ctx.send('File size is too big!')

    @cog_ext.cog_slash(name="chemist",
                       guild_ids=guild_ids_list,
                       description='sends info about server',
                       options=[
                           create_option(name='x',
                                         option_type=3,
                                         required=True,
                                         description='your 1st argument'),
                           create_option(name='y',
                                         option_type=3,
                                         required=True,
                                         description='your 2nd argument')
                       ])
    async def chemist(self, ctx, x, y):
        """returnrs chemical reaction equation"""
        out = func.parser(x, y)
        x = self.bot.get_emoji(837943828505559070)
        embed = discord.Embed(
            title='Done' + ' ' + str(x),
            description=out,
            colour=discord.Colour.from_rgb(r.randint(200, 255), r.randint(200, 255), r.randint(200, 255))
        )
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name='gradient',
                       guild_ids=guild_ids_list,
                       description='sends random gradient image, arguments: 2/3 numbers of colors',
                       options=[
                           create_option(
                               name='color1',
                               option_type=3,
                               required=True,
                               description='color at the begin of gradient',
                           ),
                           create_option(
                               name='color2',
                               option_type=3,
                               required=True,
                               description='color at the middle/end of gradient',
                           ),
                           create_option(
                               name='color3',
                               option_type=3,
                               required=False,
                               description='color at the end of gradient',
                           )
                       ])
    async def gradient(self, ctx: SlashContext, color1: str, color2: str, color3=False):
        try:
            color1 = list(map(int, color1.split()))
            color2 = list(map(int, color2.split()))
            if color3:
                color3 = list(map(int, color3.split()))
            grad = func.gradient(color1, color2, color3)
            with io.BytesIO() as image_binary:
                grad.save(image_binary, 'PNG')
                image_binary.seek(0)
                await ctx.send(file=discord.File(fp=image_binary, filename='image.png'))
        except:
            await ctx.send(embed=discord.Embed(title='**SOMETHING WENT WRONG**', description= 'It\'s seems like you '
                                                                                              'insert wrong command(( '
                                                                                              '\n\n**Example of '
                           'command:** \n /gradient color1: 255 150 0 color2: 255 0 255 color3: 0 255 255 \n'
                           '/gradient color1: 255 150 0 color2: 255 0 255',
                                               color=discord.Color.from_rgb(r.randint(100, 200),
                                                                            r.randint(100, 200), r.randint(100, 200))))

    @cog_ext.cog_slash(name='avatar',
                       guild_ids=guild_ids_list,
                       description='sends user avatar',
                       options=[
                           create_option(
                               name='member',
                               option_type=6,
                               required=False,
                               description='user which avatar you wanna see',
                           )
                       ])
    async def avatar(self, ctx: SlashContext, member=None):
        if member is None:
            member = ctx.author
        embed = discord.Embed(title=f'{member}\'s avatar')
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name='shifrovalus',
                       guild_ids=guild_ids_list,
                       description='turns string into code',
                       options=[
                           create_option(
                               name='shifr',
                               option_type=3,
                               required=True,
                               description='not shifr',
                           )
                       ])
    async def shifrovalus(self, ctx: SlashContext, *, shifr):
        okonchnius = ['ус', 'инатор', 'ъ', 'миум']
        s = ''
        for i in shifr.split():
            s += i + r.choice(okonchnius) + ' '
        await ctx.send(s)

    @cog_ext.cog_slash(name='userinfo',
                       guild_ids=guild_ids_list,
                       description='returns info about user',
                       options=[
                           create_option(
                               name='user',
                               option_type=6,
                               required=False,
                               description='not shifr',
                           )
                       ])
    async def userinfo(self, ctx: SlashContext, user: discord.Member = None):  # b'\xfc'
        if user is None:
            user = ctx.author
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(color=0xdfa3ff, description=user.mention)
        embed.set_author(name=str(user), icon_url=user.avatar_url)
        embed.set_thumbnail(url=user.avatar_url)
        embed.add_field(name="Joined", value=user.joined_at.strftime(date_format))
        members = sorted(ctx.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Join position", value=str(members.index(user) + 1))
        embed.add_field(name="Registered", value=user.created_at.strftime(date_format))
        if len(user.roles) > 1:
            role_string = ' '.join([r.mention for r in user.roles][1:])
            embed.add_field(name="Roles [{}]".format(len(user.roles) - 1), value=role_string, inline=False)
        perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in user.guild_permissions if p[1]])
        embed.add_field(name="Guild permissions", value=perm_string, inline=False)
        embed.set_footer(text='ID: ' + str(user.id))
        return await ctx.send(embed=embed)

    # @cog_ext.cog_slash(name='archive',
    #                    guild_ids=guild_ids_list,
    #                    description='archives chat messages into DMs',
    #                    options=[
    #                        create_option(
    #                            name='number',
    #                            option_type=4,
    #                            required=True,
    #                            description='number of messages',
    #                        )
    #                    ])
    # async def archive(self, ctx: SlashContext, number):
    #     messages = await ctx.channel.history(limit=number).flatten()
    #     await ctx.author.send(embed=discord.Embed(title=datetime.datetime.now(),
    #                                               color=discord.Color.from_rgb(255, 0, 255)))
    #     for i in messages:
    #         member = ctx.guild.get_member(i.author.id)
    #         if member != None:
    #             higest = discord.utils.find(lambda role: role in member.roles, reversed(member.roles))
    #             color = higest.color
    #         else:
    #             color = discord.Color.from_rgb(255, 255, 255)
    #         await ctx.author.send(embed=discord.Embed(title=i.author, description=i.content, color=color))


def setup(bot):
    bot.add_cog(MainCog(bot))

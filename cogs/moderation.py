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
import json


class MainCog(commands.Cog, name='moderation'):
    '''commands for moderators'''
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str):
        '''bans member'''
        await ctx.send(embed=discord.Embed(title=f'Are you sure you want to ban {member} for {reason}?'),
                       components=[
                           Button(label="Ban member", style=ButtonStyle.blue)
                       ])
        i = await self.bot.wait_for("button_click")
        if i:
            await i.respond(content=f'{member} was banned!')
            await member.ban(reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, id):
        '''unbans member'''
        user = await self.bot.fetch_user(id)
        await ctx.send(embed=discord.Embed(title=f'Are you sure you want to unban {user}?', color=0x00ff00),
                       components=[
                           Button(label="Unban member", style=ButtonStyle.blue)
                       ])
        i = await self.bot.wait_for("button_click")
        if i:
            try:
                await ctx.guild.unban(user)
                await i.respond(content=f'{user} was unbanned!')
            except:
                await i.respond(content=f'{user} is not banned rn)')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str):
        '''kicks member'''
        await ctx.send(embed=discord.Embed(title=f'Are you sure you want to kick {member} for {reason}?'),
                       components=[
                           Button(label="✔", style=ButtonStyle.blue)
                       ])
        i = await self.bot.wait_for("button_click")
        if i:
            await i.respond(content=f'{member} was kicked')
            await member.kick(reason=reason)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member:discord.Member):
        '''gives member role with name contains \"mute\"'''
        for i in ctx.message.guild.roles:
            if 'mute' or 'MUTE' in str(i):
                await member.give_role(i)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def setjoinrole(self, ctx, role):
        """set role that member will get when he joined server"""
        guild = ctx.message.guild
        role = discord.utils.get(guild.roles, name=role)
        functions.updatesql(server=ctx.guild.id, joinrole=role.id)
        await ctx.send(embed=discord.Embed(title='Sucsess!', color=discord.Colour.from_rgb(255, 0, 255)))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setjoinlogchannel(self, ctx, channel):
        """set cahnnel when you can view who entered your server and how"""
        guild = ctx.message.guild
        channel = discord.utils.get(guild.channels, name=channel)
        functions.updatesql(server=ctx.guild.id, joinchannel=channel.id)
        await ctx.send(embed=discord.Embed(title='Sucsessful!'))

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def setlogs(self, ctx, channel):
        """set logs channel"""
        guild = ctx.message.guild
        channel = discord.utils.get(guild.channels, name=channel)
        functions.updatesql(server=ctx.guild.id, logs=channel.id)
        await ctx.send(embed=discord.Embed(title='Sucsessful!', color=0x5fe9dd))


def setup(bot):
    bot.add_cog(MainCog(bot))
import datetime
import random
import discord
from discord.ext import commands, tasks
from discord_components import DiscordComponents
from discord_slash import SlashCommand
import functions
import json

token = your token

i = discord.Intents().all()
bot = commands.Bot(command_prefix='..', intents=i)
slash = SlashCommand(bot, sync_commands=True)

guild_ids_list = []
invites = {}

bot.remove_command('help')
initial_extensions = [
    'cogs.help',
]
bot.load_extension('cogs.help')
bot.load_extension("cogs.slashcog")
bot.load_extension("cogs.moderation")
bot.load_extension('cogs.fun')
bot.load_extension('cogs.filters')
bot.load_extension('cogs.messagefilters')


@bot.command()
async def add(ctx, a: int, b: int):
    """slove 1 argument + 2 argument"""
    await ctx.send(a + b)


@bot.command()
@commands.has_permissions(administrator=True)
async def createjoins(ctx, *, category):
    guild = ctx.message.guild
    cat = discord.utils.get(guild.categories, name=category)
    ch = await guild.create_voice_channel('Join to create', category=cat)
    functions.updatesql(server=ctx.guild.id, joinvoice=ch.id, voicecat=cat.id)
    await ctx.send(embed=discord.Embed(title='Sucsessful!'))


@bot.event
async def on_voice_state_update(member, before, after):
    if after:
        if after.channel:
            try:
                data, cat = functions.getsqldata(server=member.guild.id, joinvoice=True)
                if after.channel.id == data:
                    guild = bot.get_guild(member.guild.id)
                    cat = discord.utils.get(guild.categories, id=cat)
                    ch = await guild.create_voice_channel(f'{member.name}\'s cahnnel', category=cat)
                    await ch.set_permissions(member, manage_channels=True, manage_permissions=True)
                    await member.move_to(ch)
                    with open('channelstodelete.txt', 'a') as f:
                        f.write(' ' + str(guild.id) + ' ' + str(ch.id) + '\n')
            except:
                pass
    if before:
        if before.channel:
            f = open('channelstodelete.txt')
            x = f.read().split()
            if str(before.channel.id) in x:
                if not before.channel.members:
                    await before.channel.delete()


@bot.event
async def on_message(message):
    await bot.process_commands(message)
    guild = message.guild
    if functions.checker(guild=guild.id):
        if functions.getsqldata(server=guild.id, links=True):
            s = message.content
            if 'www' in s or 'http' in s:
                try:
                    if functions.checklink(s):
                        await message.delete()
                        print('deleted!')
                except Exception as e:
                    print(e)
    if guild == None:
        pass
    elif guild.id == 679870413140262944:
        try:
            lang = functions.checklang(message.content)
            if lang == 'ru' or lang == 'mk' or lang == 'bg' or lang == 'uk':
                role = discord.utils.get(guild.roles, name="Russian")
                user = guild.get_member(message.author.id)
                for i in user.roles:
                    if i.id == 681944762076626985 or i.id == 682169503429296149:
                        return
                await user.add_roles(role)
            else:
                role = discord.utils.get(guild.roles, name="Foreigner")
                user = guild.get_member(message.author.id)
                for i in user.roles:
                    if i.id == 682169503429296149 or i.id == 681944762076626985:
                        return
                await user.add_roles(role)
        except:
            pass


@bot.event
async def on_member_join(member):
    datac = functions.getsqldata(server=member.guild.id, joinchannel=True)
    channel = discord.utils.get(member.guild.channels, id=datac)
    if functions.checker(guild=member.guild.id):
        invites_before_join = invites[member.guild.id]
        invites_after_join = await member.guild.invites()
        for i in invites_before_join:
            for j in invites_after_join:
                if i.uses == j.uses - 1 and i.code == j.code:
                    invite = j
                    break
        invites_after_join = await member.guild.invites()
        date_format = "%a, %d %b %Y %I:%M %p"
        embed = discord.Embed(color=0xdfa3ff, description=member.mention)
        embed.set_author(name=str(member), icon_url=member.avatar_url)
        embed.set_thumbnail(url=member.avatar_url)
        members = sorted(member.guild.members, key=lambda m: m.joined_at)
        embed.add_field(name="Join position", value=str(members.index(member) + 1))
        embed.add_field(name="Registered", value=member.created_at.strftime(date_format))
        embed.add_field(name="Invite Code", value=invite.code)
        embed.add_field(name="Inviter", value=invite.inviter)
        if len(member.roles) > 1:
            role_string = ' '.join([r.mention for r in member.roles][1:])
            embed.add_field(name="Roles [{}]".format(len(member.roles) - 1), value=role_string, inline=False)
        perm_string = ', '.join([str(p[0]).replace("_", " ").title() for p in member.guild_permissions if p[1]])
        embed.add_field(name="Guild permissions", value=perm_string, inline=False)
        embed.set_footer(text='ID: ' + str(member.id))
        await channel.send(embed=embed)
        invites[member.guild.id] = invites_after_join
    if member.guild.id == 679870413140262944:
        if int(str(datetime.datetime.now() - member.created_at).split()[0]) <= 20:
            role = discord.utils.get(member.guild.roles, name="rip")
            await member.add_roles(role)
            return
    data = functions.getsqldata(server=member.guild.id, joinrole=True)
    try:
        role = discord.utils.get(member.guild.roles, id=data)
        await member.add_roles(role)
    except:
        pass


#logs events
@bot.event
async def on_message_delete(message):
    guild = message.guild
    if functions.checker(guild=guild.id):
        ch = functions.getsqldata(server=guild.id, logs=True)
        if ch:
            date_format = "%a, %d %b %Y %I:%M %p"
            a = str("""```diff\n-{}{}```""".format(message.content, ' ' * (100 - len(message.content))))
            channel = discord.utils.get(guild.channels, id=ch)
            embed = discord.Embed(title='Message was deleted!',
                                  description='**Content:** \n' + a, color=0xfb0350)
            embed.set_author(name=str(message.author), icon_url=message.author.avatar_url)
            embed.add_field(name='Channel:', value=f'{message.channel}\n<#{message.channel.id}>')
            embed.set_footer(text=str(datetime.datetime.now().__format__(date_format)))
            await channel.send(embed=embed)


@bot.event
async def on_message_edit(before, after):
    guild = after.guild
    if functions.checker(guild=guild.id):
        ch = functions.getsqldata(server=guild.id, logs=True)
        if ch:
            date_format = "%a, %d %b %Y %I:%M %p"
            b = str("""```fix\n{}{}```""".format(before.content, ' ' * (100 - len(after.content))))
            a = str("""```yaml\n{}{}```""".format(after.content, ' ' * (100 - len(after.content))))
            channel = discord.utils.get(guild.channels, id=ch)
            embed = discord.Embed(description=f'[Message](https://discord.com/channels/{guild.id}/{after.channel.id}/{after.id}) was edited!',
                                  color=0x5ce8c2)
            embed.add_field(name='Content before:',
                            value=b, inline=False)
            embed.add_field(name='Content after:',
                            value=a, inline=False)
            embed.set_author(name=str(after.author), icon_url=after.author.avatar_url)
            embed.add_field(name='Channel:', value=f'{after.channel}\n<#{after.channel.id}>')
            embed.set_footer(text=str(datetime.datetime.now().__format__(date_format)))
            await channel.send(embed=embed)


@bot.event
async def on_member_ban(guild, member):
    if functions.checker(guild=guild.id):
        ch = functions.getsqldata(server=guild.id, logs=True)
        if ch:
            date_format = "%a, %d %b %Y %I:%M %p"
            channel = discord.utils.get(guild.channels, id=ch)
            logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.ban).flatten()
            logs = logs[0]
            if logs.target == member:
                embed = discord.Embed(title=f'{member} was banned!', color=0xbf1562)
                embed.add_field(name='Moderator:', value=logs.user.mention)
                embed.add_field(name='Reason:', value=logs.reason)
                embed.set_footer(text=str(logs.created_at.__format__(date_format)))
                await channel.send(embed=embed)


@bot.event
async def on_member_kick(member):
    guild = member.guild
    if functions.checker(guild=guild.id):
        ch = functions.getsqldata(server=guild.id, logs=True)
        if ch:
            date_format = "%a, %d %b %Y %I:%M %p"
            channel = discord.utils.get(guild.channels, id=ch)
            logs = await guild.audit_logs(limit=1, action=discord.AuditLogAction.kick).flatten()
            logs = logs[0]
            if logs.target == member:
                embed = discord.Embed(title=f'{member} was kicked!', color=0x17838a)
                embed.add_field(name='Moderator:', value=logs.user)
                embed.add_field(name='Reason:', value=logs.reason)
                embed.set_footer(text=str(logs.created_at.__format__(date_format)))
                await channel.send(embed=embed)


@bot.event
async def on_ready():
    DiscordComponents(bot)
    for guild in bot.guilds:
        try:
            guild_ids_list.append(guild.id)
            invites[guild.id] = await guild.invites()
        except:
            pass
    await bot.change_presence(activity=discord.Game('..help for help'))



bot.run(token)

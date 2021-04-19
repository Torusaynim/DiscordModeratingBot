import os
import discord
import random
from discord.ext import commands
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='>', intents=intents)

# Перенести в будущем в отдельный файл по возможности
bad_words = ['дурак', 'идиот', 'лох']

stats = {}


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')


@bot.command()
async def hello(ctx):
    """
    Greet your faithful bot

    Args:
        ctx: context command was used in
    """
    await ctx.send('Hello!')


@bot.command()
async def roll(ctx, dice: str):
    """
    Simulate dice throw

    Args:
        ctx: context command was used in
        dice: string in NdN format

    Returns:
        on exception throw
    """
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return
    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.event
async def on_message_delete(message):
    """
    Deleted messages processing

    Args:
        message: deleted message context
    """
    channel = bot.get_channel(430432809371435008)
    embed = discord.Embed(description='', colour=0xD5A6BD)
    attachments = message.attachments
    if message.content:
        embed.add_field(name="Deleted message: ", value=message.content, inline=False)
    if attachments:
        embed.set_image(url=attachments[0].url)

    embed.add_field(name="Author: ", value=str(message.author), inline=False)
    embed.add_field(name="Channel: ", value=str(message.channel), inline=False)
    embed.add_field(name="Time: ", value=str(message.created_at) + ", UMT", inline=False)
    await channel.send(embed=embed)
    # исправить время удаленного сообщения (добавить автора удаления сообщения)


@bot.event
async def on_message(message):
    """
    Sent messages processing

    Args:
        message: sent message context
    """
    flag = True
    for word in message.content.lower().split():
        for restricted in bad_words:
            if word == restricted:
                await message.delete()
                flag = False
    if flag is True:
        if stats.get(str(message.author)):
            stats[str(message.author)] = stats[str(message.author)] + 1
        else:
            stats[str(message.author)] = 1
    await bot.process_commands(message)


@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, user: discord.Member):
    """
    Kick user from the server

    Args:
        ctx: text channel context command was used in
        user: user mention(@ping)
    """
    await ctx.guild.kick(user)


@bot.command()
async def meme(ctx):
    """
    Replies with a random picture from the folder

    Args:
        ctx: context command was used in
    """
    await ctx.channel.send(file=discord.File("img\\" + random.choice(os.listdir("img"))))


@bot.command()
async def anon(ctx, *, message=""):
    """
    Sends anon message from bot's perspective

    Args:
        ctx: context command was used in
        message: message text
    """
    channel = bot.get_channel(669481745435066398)
    embed = discord.Embed(description='', colour=0xD5A6BD)
    embed.add_field(name="Anon message", value="User " + str(ctx.author.id) + ": " + message, inline=False)
    if ctx.message.attachments:
        embed.set_image(url=ctx.message.attachments[0].url)
    await channel.send(embed=embed)


@bot.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, number):
    """
    Erase last N messages

    Args:
        ctx: context command was used in
        number: number of messages to be erased
    """
    await ctx.channel.purge(limit=int(number))


@bot.command()
@commands.has_permissions(administrator=True)
async def addrole(ctx, user: discord.Member, role: discord.Role):
    """
    Give specific user specific role

    Args:
        ctx: context command was used in
        user: user mention(@ping)
        role: role mention(@ping)
    """
    await user.add_roles(role)
    await ctx.send(f"{user.name} got a role called: {role.name} by {ctx.author.name}")


@bot.command()
async def stat(ctx):
    """
    Reply with sent messages stat

    Args:
        ctx: context command was used in
    """
    embed = discord.Embed(description='', colour=0xD5A6BD)
    for key, value in stats.items():
        embed.add_field(name=key + ": ", value=str(value) + " messages", inline=False)
    await ctx.send(embed=embed)


@bot.command()
async def join(ctx):
    """
    Make bot join VC

    Args:
        ctx: context command was used in
    """
    channel = ctx.author.voice.channel
    await channel.connect()


@bot.command()
async def allmute(ctx):
    """
    Mute all users of the voice chat

    Args:
        ctx: context command was used in
    """
    vc = ctx.author.voice.channel
    for member in vc.members:
        await member.edit(mute=True)


@bot.command()
async def allunmute(ctx):
    """
    Unmute all users of the voice chat

    Args:
        ctx: context command was used in
    """
    vc = ctx.author.voice.channel
    for member in vc.members:
        await member.edit(mute=False)


@bot.command()
async def mute(ctx, user: discord.Member):
    """
    Disable users's ability to speak in VC

    Args:
        ctx: context command was used in
        user: user mention(@ping)
    """
    vc = ctx.author.voice.channel
    await user.edit(mute=True)

bot.run(TOKEN)
import discord
import os
from discord import Embed
from dotenv import load_dotenv

load_dotenv()

from discord.ext import commands

bot = commands.Bot(command_prefix=",", intents=discord.Intents.all(), help_command=None)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.command()
async def hello(ctx):
    await ctx.send('Hello, World!')

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! Latency: {round(bot.latency * 1000)}ms')


@bot.command(name="av")
async def avatar(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author

    embed = Embed(
        title = f"{member.name}'s avatar",
        url = member.avatar,
        color = member.color
        ).set_image(url = member.avatar.url)
    await ctx.send(embed=embed)

TOKEN = os.getenv('TOKEN')


bot.run(TOKEN)


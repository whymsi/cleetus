import discord
import os
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

TOKEN = os.getenv('TOKEN')


bot.run(TOKEN)


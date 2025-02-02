import aiosqlite.context
import discord
import os
from discord.ext import commands
from dotenv import load_dotenv
import aiosqlite
from db import *
from cogs.help import EmbedHelpCommand


load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

bot = commands.Bot(
    command_prefix=get_prefix,
    intents=discord.Intents.all()
)

async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')
    print("loading resources...")

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

    bot.db = await aiosqlite.connect("prefixes.db")
    
    async with bot.db.cursor() as cursor:
        await cursor.execute('CREATE TABLE IF NOT EXISTS prefixes (prefix TEXT, guild ID)')
        await bot.db.commit()

        await load()
    
    await bot.tree.sync()
    print("Cogs loaded!")

    print("Database connected.")

@bot.command(aliases=['off'])
@commands.is_owner()  # Ensures only the bot owner can shut it down
async def shutdown(ctx):
    """Shuts down the bot gracefully."""
    try:
        await ctx.send("Shutting down the bot...")  # Inform the user
        
        # Close any open resources, like HTTP or database connections
        if hasattr(bot, "db"):
            await bot.db.close()
            print("Database connection closed.")
        
        # Gracefully close the HTTP session used by discord.py
        await bot.http.close()
        print("HTTP connection closed.")
        
        # Now shut down the bot itself
        await bot.close()
        print("Bot shut down successfully.")
    
    except Exception as e:
        print(f"Error during shutdown: {e}")
        await ctx.send(f"Error occurred while shutting down: {e}")

bot.help_command = EmbedHelpCommand()

bot.run(TOKEN)
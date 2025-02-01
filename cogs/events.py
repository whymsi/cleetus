import discord
from discord.ext import commands, tasks
from itertools import cycle
import aiosqlite

from db import *

class Events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.statuses = cycle(
            [
                ("watching", lambda: f"{len(bot.guilds)} servers"),
                ("listening", lambda: f" {len(bot.users)} members"),
            ]
        )
        self.activity_id = {
            "playing": discord.ActivityType.playing,
            "streaming": discord.ActivityType.streaming,
            "listening": discord.ActivityType.listening,
            "watching": discord.ActivityType.watching
        }

    async def cog_load(self):
        """Start the status loop when the cog is loaded."""
        self.status_loop.start()

    async def cog_unload(self):
        """Cancel the status loop when the cog is unloaded."""
        self.status_loop.cancel()

    @tasks.loop(minutes=3.0)
    async def status_loop(self):
        """Periodically change the bot's presence."""
        await self.next_status()

    @status_loop.before_loop
    async def task_waiter(self):
        """Wait until the bot is ready before starting the loop."""
        await self.bot.wait_until_ready()

    async def next_status(self):
        """Switch to the next status message."""
        activity_type, status_func = next(self.statuses)
        await self.bot.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                type=self.activity_id[activity_type],
                name=status_func(),
            ),
        )

@commands.Cog.listener()
async def on_guild_join(guild):
    async with aiosqlite.connect("prefixes.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('INSERT INTO prefixes (prefix, guild) VALUES (?,?)', (',', guild.id,))
        await db.commit() # Ensure it works

@commands.Cog.listener()
async def on_guild_remove(guild):
    async with aiosqlite.connect("prefixes.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('DELETE FROM prefixes WHERE guild = ?', (guild.id,))
        await db.commit()  # Ensure deletion is saved

async def setup(bot):
    await bot.add_cog(Events(bot))
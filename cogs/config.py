import discord
from discord.ext import commands
import aiosqlite

class Config(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='setprefix', description="Set a custom prefix for the server.", aliases=['prefix'],)
    @commands.has_permissions(administrator=True)  # Only allow administrators to change the prefix
    async def setprefix(self, ctx, prefix=None):
        """Sets a custom prefix for the current server."""
        
        # If no prefix is provided, prompt the user
        if prefix is None:
            await ctx.send('Please provide a new prefix to set.')
            return

        # Check if prefix is too long (optional check)
        if len(prefix) > 5:
            await ctx.send("Prefix is too long. Maximum length is 5 characters.")
            return

        # Connect to the SQLite database asynchronously using aiosqlite
        async with aiosqlite.connect("prefixes.db") as db:
            async with db.cursor() as cursor:
                # Check if the guild already has a custom prefix
                await cursor.execute('SELECT prefix FROM prefixes WHERE guild = ?', (ctx.guild.id,))
                data = await cursor.fetchone()

                if data:
                    # Update the existing prefix for the guild
                    await cursor.execute('UPDATE prefixes SET prefix = ? WHERE guild = ?', (prefix, ctx.guild.id))
                    await ctx.send(f'Updated prefix to **{prefix}** for this server.')
                else:
                    # If no prefix exists, insert a new one
                    await cursor.execute('INSERT INTO prefixes (prefix, guild) VALUES (?, ?)', (prefix, ctx.guild.id))
                    await ctx.send(f'Set the prefix to **{prefix}** for this server.')

            # Commit the changes to the database
            await db.commit()

    @setprefix.error
    async def setprefix_error(self, ctx, error):
        """Error handler for the setprefix command."""
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to change the prefix. Only administrators can do that.")
        else:
            await ctx.send(f"An error occurred: {error}")


async def setup(bot):
    await bot.add_cog(Config(bot))
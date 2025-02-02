import discord
from discord.ext import commands


class EmbedHelpCommand(commands.HelpCommand):
    ...


async def setup(bot):
    bot.help_command == EmbedHelpCommand()    

import aiosqlite.context
import discord
import os
from discord.ext import commands
from discord import Embed
from dotenv import load_dotenv
import aiosqlite

from db import *

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')


bot = commands.Bot(
    command_prefix=get_prefix,
    intents=discord.Intents.all()
)

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')
    async with aiosqlite.connect("prefixes.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('CREATE TABLE IF NOT EXISTS prefixes (prefix TEXT, guild ID)')
        await db.commit()

@bot.event
async def on_guild_join(guild):
    async with aiosqlite.connect("prefixes.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('INSERT INTO prefixes (prefix, guild) VALUES (?,?)', (',', guild.id,))
        await db.commit() # Ensure it works

@bot.event
async def on_guild_remove(guild):
    async with aiosqlite.connect("prefixes.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('DELETE FROM prefixes WHERE guild = ?', (guild.id,))
        await db.commit()  # Ensure deletion is saved

@bot.command()
async def hello(ctx):
    await ctx.send('Hello, World!')

@bot.command()
async def ping(ctx):
    await ctx.send(f'Pong! Latency: {round(bot.latency * 1000)}ms')


@bot.command(aliases=['av'])
async def avatar(ctx, member: discord.Member = None):
    if not member:
        member = ctx.author

    av_embed = Embed(
        title = f"{member.name}'s avatar",
        url = member.avatar,
        color = member.color
        ).set_image(url = member.avatar.url)
    await ctx.send(embed=av_embed)

@bot.command(aliases=['b'])
async def banner(ctx, *, user: discord.Member = None):
    if not user:
        u = ctx.author
    else:
        u = user
    member = await bot.fetch_user(u.id)
    userBannerUrl = member.banner

    ba_embed = Embed(
        title = f"{member.name}'s banner",
        url = member.banner,
        color = member.color
        ).set_image(url = f"{userBannerUrl}")
    
    no_ba_embed = Embed(
        description = f"❌ | Could not find **{member.name}**'s banner.",
        color = discord.Color.red()
        )
    if member.banner is not None:
        await ctx.send(embed=ba_embed)
    else:
        await ctx.send(embed=no_ba_embed)

@bot.command()
async def setprefix(ctx, prefix=None):
    if prefix is None:
        return
    async with aiosqlite.connect("prefixes.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('SELECT prefix FROM prefixes WHERE guild = ?', (ctx.guild.id,))
            data = await cursor.fetchone()
            if data:
                await cursor.execute('UPDATE prefixes SET prefix = ? WHERE guild = ?', (prefix, ctx.guild.id,))
                await ctx.send(f'updated prefix to **{prefix}**')
            else:
                await cursor.execute('INSERT INTO prefixes (prefix, guild) VALUES (?,?)', (',', ctx.guild.id,))
                await cursor.execute('SELECT prefix FROM prefixes WHERE guild = ?', (ctx.guild.id,))
                data = await cursor.fetchone()
                if data:
                    await cursor.execute('UPDATE prefixes SET prefix = ? WHERE guild = ?', (prefix, ctx.guild.id,))
                    await ctx.send(f'updated prefix to **{prefix}**')
                return
        await db.commit()


bot.run(
    TOKEN
)


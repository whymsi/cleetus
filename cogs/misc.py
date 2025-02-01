import discord
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send('Hello, World!')

    @commands.command()
    async def ping(self, ctx):
        await ctx.send(f'Pong! Latency: {round(self.bot.latency * 1000)}ms')

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        av_embed = discord.Embed(
            title = f"{member.name}'s avatar",
            url = member.avatar,
            color = member.color
        ).set_image(url = member.avatar.url)
        await ctx.send(embed=av_embed)

    @commands.command(aliases=['b'])
    async def banner(self, ctx, *, user: discord.Member = None):
        if not user:
            u = ctx.author
        else:
            u = user
        member = await self.bot.fetch_user(u.id)
        userBannerUrl = member.banner

        ba_embed = discord.Embed(
            title = f"{member.name}'s banner",
            url = member.banner,
            color = member.color
        ).set_image(url = f"{userBannerUrl}")
        
        no_ba_embed = discord.Embed(
            description = f"❌ | Could not find **{member.name}**'s banner.",
            color = discord.Color.red()
        )
        if member.banner is not None:
            await ctx.send(embed=ba_embed)
        else:
            await ctx.send(embed=no_ba_embed)


async def setup(bot):
    await bot.add_cog(Misc(bot))
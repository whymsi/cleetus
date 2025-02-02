import discord
from discord.ext import commands
from discord import Guild

from embeds import *

OWNER_ID = 123456789012345678

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

    @commands.command(name="serverinfo", aliases=['server'])
    async def server_info(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        guild = member.guild
        humans = [member for member in ctx.guild.members if not member.bot]
        bots = [member for member in ctx.guild.members if member.bot]
        server_embed = discord.Embed(title = f"{guild.name}'s info",
            description=
                        f"**Roles:** {len(guild.roles) - 1}\n"
                        f"**Members:** {len(guild.members)}\n"
                        f"**Creation Date:** {guild.created_at.strftime('%m/%d/%Y')}",
            color = discord.Color.blue()

        ).set_thumbnail(url = guild.icon.url if guild.icon else "")
        server_embed.add_field(name="**Owner**", value=f"{guild.owner}", inline=True)
        server_embed.add_field(
            name=f"**Members**",
            value=
                f"""**Total**: {guild.member_count}
                **Humans**: {len(humans)}
                **Bots**: {len(bots)}""",
            inline=True)
        server_embed.add_field(
            name="**Channels**",
            value=f"**Text:** {len([channel for channel in guild.channels if channel.type == discord.ChannelType.text])}\n"
                    f"**Voice:** {len([channel for channel in guild.channels if channel.type == discord.ChannelType.voice])}\n"
                    f"**Category:** {len([channel for channel in guild.channels if channel.type == discord.ChannelType.category])}\n",
            inline=True)
        server_embed.add_field(
            name="**Emojis**",
            value=f"**Total:** {len(guild.emojis)}\n"
                    f"**Custom:** {len([emoji for emoji in guild.emojis if not emoji.managed])}\n"
                    f"**Managed:** {len([emoji for emoji in guild.emojis if emoji.managed])}",
                inline=True)
            
        await ctx.send(embed=server_embed)

    @commands.hybrid_command(name="info", descrption="Look up a discord member!")
    async def information(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        info_embed = discord.Embed(
            description="hello"
        ).set_author(name=f"{member.display_name} ({member.id})", icon_url=member.avatar)
        
        await ctx.send(embed=info_embed)


async def setup(bot):
    await bot.add_cog(Misc(bot))
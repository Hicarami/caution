import discord
import json
import random

from discord import app_commands
from requests import get as GET
from discord.ext import commands

def GetGifs(search_term, gif_count):
    l = []
    a = json.loads(GET(f"https://g.tenor.com/v1/search?q={search_term}&key=7VP6PF2CTRXU&limit={gif_count}").content)
    for item in a["results"]:
        l.append(item["media"][0]["gif"]["url"])
    return l

huggifs = GetGifs("anime hug", 20)
kissgifs = GetGifs("anime kiss", 20)
killgifs = GetGifs("anime kill", 20)




class FUN(commands.Cog, name="fun"):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(name="hug", description="Hug your friends! :D")
    async def hug(self, ctx, user: discord.Member) -> None:
        embed = discord.Embed(
            description = f"{ctx.author.mention} has hugged {user.mention}",
            color = ctx.author.color.value
        )
        randomgif = random.choice(huggifs)
        embed.set_image(url = randomgif)
        await ctx.reply(embed=embed)

    @commands.hybrid_command(name="kiss", description="Kiss your love <3")
    async def kiss(self, ctx, user: discord.Member) -> None:
        embed = discord.Embed(
            description = f"{ctx.author.mention} has kissed {user.mention}",
            color = ctx.author.color.value
        )
        randomgif = random.choice(kissgifs)
        embed.set_image(url = randomgif)
        await ctx.reply(embed=embed)

    @commands.hybrid_command(name="kill", description="Kill someone >:(")
    async def kill(self, ctx, user: discord.Member) -> None:
        embed = discord.Embed(
            description = f"{ctx.author.mention} has killed {user.mention}",
            color = ctx.author.color.value
        )
        randomgif = random.choice(killgifs)
        embed.set_image(url = randomgif)
        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(FUN(bot))

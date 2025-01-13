import discord
import os
import time


from discord import app_commands
from discord.ext import commands



class MISC(commands.Cog, name="misc"):
    def __init__(self, bot):
        self.bot = bot



    # embed command(create embed with your specific settings)
    @commands.hybrid_command(name="embed", description="Bot will create a embed")
    @discord.app_commands.describe(title="The title of the embed", description="The description of the embed")
    async def embed(self, ctx: commands.Context, title: str, description: str):
        embd = discord.Embed(
            title= title,
            description= description
        )
        await ctx.reply(embed=embd)


    @commands.hybrid_command(name="ping", description="Ping the bot")
    async def ping(self, ctx):
        start = time.perf_counter()
        message = await ctx.send("Resolving...")
        end = time.perf_counter()
        
        # Calculate response time
        duration = (end - start) * 1000
        
        # Create an embed for the response
        embed = discord.Embed(title="Ping Response", color=discord.Color.green())
        embed.add_field(name="Web Socket Latency", value=f"{round(self.bot.latency * 1000)}ms", inline=False)
        embed.add_field(name="Total Latency", value=f"{duration:.0f}ms", inline=False)
        
        # Edit the message to include the embed
        await message.edit(content=None, embed=embed)
        
        



async def setup(bot):
    await bot.add_cog(MISC(bot))
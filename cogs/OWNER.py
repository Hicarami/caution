import discord
import os
import json
from discord.ext import commands

if not os.path.isfile("config.json"):
    sys.exit("'config.json' not found! Please add it and try again.")
else:
    with open("config.json") as file:
        config = json.load(file)


class AdminCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name='clearbotmessages', help="Clears all messages the bot has sent in this DM.")
    async def clear_bot_messages(self, ctx):
        """Clears all the messages the bot has sent in the DM channel."""

        if not isinstance(ctx.channel, discord.DMChannel):
            await ctx.send("This command can only be used in DMs.")
            return

        # Check the DM channel and delete messages sent by the bot
        deleted = 0
        async for message in ctx.channel.history(limit=100):  # Increase limit if needed
            if message.author == self.bot.user:
                await message.delete()
                deleted += 1

        await ctx.send(f"🧹 Deleted {deleted} messages sent by the bot.", delete_after=5)  # Notify user, then delete this message after 5 seconds



# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(AdminCog(bot))

